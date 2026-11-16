"""Gera LI, Manual e CCI em .docx a partir de um conteúdo em JSON, sobre as bases de templates/.

A base fornece capa, cabeçalho, rodapé e estilos; este módulo escreve o corpo.
Formato do conteúdo: ver skills/*/references/conteudo.md.

Marcação dentro de textos:  **negrito**   `código`   [[trecho a revisar]] (amarelo)
"[PREENCHER: ...]" sai sempre em amarelo. Bloco/seção com "revisar": true sai inteiro em amarelo.
"""
import json, os, re

from docx import Document
from docx.enum.text import WD_BREAK, WD_COLOR_INDEX
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.shared import Cm, Pt
from docx.table import _Cell
from docx.text.paragraph import Paragraph
from docx.text.run import Run

from .indices import raiz_padrao

TIPOS = ('li', 'manual', 'cci')
IDIOMAS = ('pt-BR', 'es')
AVISO = {'pt-BR': 'O que está em amarelo no documento cabe análise do consultor.',
         'es': 'Lo que está en amarillo en el documento requiere análisis del consultor.'}
PREENCHER = {'pt-BR': 'PREENCHER', 'es': 'COMPLETAR'}

# valor de segredo depois de "senha:", "token=", "Bearer " etc. (regra de segurança: nunca vai ao documento)
_SEGREDO = re.compile(
    r'(?i)\b(senha|password|passwd|pwd|contrase[nñ]a|secret|client[_-]?secret|api[_-]?key|token|access[_-]?token|authorization)'
    r'("?\s*[:=]\s*"?)(?!\*)(?:Bearer\s+|Basic\s+)?([A-Za-z0-9+/_\-.=~]{8,})|\b(Bearer|Basic)\s+([A-Za-z0-9+/_\-.=~]{12,})')
_INLINE = re.compile(r'(\[\[.+?\]\]|\*\*.+?\*\*|`[^`]+`|\[(?:PREENCHER|COMPLETAR)[^\]]*\])', re.S)


def mascarar(texto):
    def troca(m):
        if m.group(4):
            return f'{m.group(4)} ********'
        valor = m.group(3)
        if not re.search(r'\d', valor) and len(valor) < 16:  # palavra comum ("token: fixo"), não segredo
            return m.group(0)
        return f'{m.group(1)}{m.group(2)}********'
    return _SEGREDO.sub(troca, texto)


class ErroConteudo(ValueError):
    pass


# ------------------------------------------------------------------ escrita de blocos
class Escritor:
    def __init__(self, doc, idioma):
        self.doc, self.idioma = doc, idioma
        self.amarelos = 0
        self._abs = {}
        self.largura = doc.sections[0].page_width - doc.sections[0].left_margin - doc.sections[0].right_margin

    # --- inline
    def runs(self, par, texto, amarelo=False, negrito=None, tamanho=None, mono=False):
        texto = mascarar(str(texto))
        for parte in _INLINE.split(texto):
            if not parte:
                continue
            am, ng, cod = amarelo, negrito, mono
            if parte.startswith('[[') and parte.endswith(']]'):
                self.runs(par, parte[2:-2], True, negrito, tamanho, mono)  # aceita `código` e **negrito** dentro do amarelo
                continue
            elif parte.startswith('**') and parte.endswith('**') and len(parte) > 4:
                parte, ng = parte[2:-2], True
            elif parte.startswith('`') and parte.endswith('`') and len(parte) > 2:
                parte, cod = parte[1:-1], True
            elif re.match(r'\[(PREENCHER|COMPLETAR)', parte):
                parte, am = re.sub(r'^\[(PREENCHER|COMPLETAR)', '[' + PREENCHER[self.idioma], parte), True
            linhas = parte.split('\n')
            for i, linha in enumerate(linhas):
                r = par.add_run(linha)
                if i < len(linhas) - 1:
                    r.add_break()
                if ng:
                    r.bold = True
                if cod:
                    r.font.name = 'Consolas'; r.font.size = Pt(9.5)
                if tamanho:
                    r.font.size = Pt(tamanho)
                if am:
                    r.font.highlight_color = WD_COLOR_INDEX.YELLOW
                    self.amarelos += 1
        return par

    def _estilo(self, *nomes):
        for n in nomes:
            try:
                return self.doc.styles[n]
            except KeyError:
                continue
        return self.doc.styles['Normal']

    # --- numeração própria para listas (as bases não trazem listas prontas)
    def _num(self, numerada):
        numbering = self.doc.part.numbering_part.element
        chave = 'n' if numerada else 'b'
        if chave not in self._abs:
            ids = [int(a.get(qn('w:abstractNumId'))) for a in numbering.findall(qn('w:abstractNum'))]
            aid = max(ids + [0]) + 1
            niveis = ''
            for lvl in range(3):
                fmt, txt, fonte = ('decimal', f'%{lvl + 1}.', '') if numerada else \
                    ('bullet', '•' if lvl == 0 else '–', '<w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/></w:rPr>')
                niveis += (f'<w:lvl w:ilvl="{lvl}"><w:start w:val="1"/><w:numFmt w:val="{fmt}"/><w:lvlText w:val="{txt}"/>'
                           f'<w:lvlJc w:val="left"/><w:pPr><w:ind w:left="{720 * (lvl + 1)}" w:hanging="360"/></w:pPr>{fonte}</w:lvl>')
            absn = parse_xml(f'<w:abstractNum {nsdecls("w")} w:abstractNumId="{aid}"><w:multiLevelType w:val="hybridMultilevel"/>{niveis}</w:abstractNum>')
            primeiro_num = numbering.find(qn('w:num'))
            ultimo_abs = numbering.findall(qn('w:abstractNum'))
            if primeiro_num is not None:
                primeiro_num.addprevious(absn)
            elif ultimo_abs:
                ultimo_abs[-1].addnext(absn)
            else:
                numbering.insert(0, absn)
            self._abs[chave] = aid
        if not numerada and 'b_num' in self._abs:
            return self._abs['b_num']
        nid = max([int(n.get(qn('w:numId'))) for n in numbering.findall(qn('w:num'))] + [0]) + 1
        num = parse_xml(f'<w:num {nsdecls("w")} w:numId="{nid}"><w:abstractNumId w:val="{self._abs[chave]}"/>'
                        f'<w:lvlOverride w:ilvl="0"><w:startOverride w:val="1"/></w:lvlOverride></w:num>')
        nums = numbering.findall(qn('w:num'))
        nums[-1].addnext(num) if nums else numbering.append(num)  # depois dos <w:num>, antes de numIdMacAtCleanup
        if not numerada:
            self._abs['b_num'] = nid
        return nid

    # --- blocos
    def paragrafo(self, alvo, texto, amarelo=False, estilo=None, **kw):
        p = alvo.add_paragraph(style=estilo or self._estilo('Normal'))
        return self.runs(p, texto, amarelo, **kw)

    def lista(self, alvo, itens, numerada=False, amarelo=False):
        nid = self._num(numerada)
        for item in itens:
            nivel = 0
            if isinstance(item, dict):
                item, nivel = item.get('texto', ''), int(item.get('nivel', 0))
            p = alvo.add_paragraph(style=self._estilo('List Paragraph'))
            ppr = p._p.get_or_add_pPr()
            ppr.append(parse_xml(f'<w:numPr {nsdecls("w")}><w:ilvl w:val="{nivel}"/><w:numId w:val="{nid}"/></w:numPr>'))
            self.runs(p, item, amarelo)

    def tabela(self, alvo, colunas, linhas, amarelo=False, larguras=None, largura_total=None):
        if not colunas:
            raise ErroConteudo('tabela sem colunas')
        for i, l in enumerate(linhas):
            if len(l) != len(colunas):
                raise ErroConteudo(f'tabela "{colunas[0]}…": linha {i + 1} tem {len(l)} células, esperado {len(colunas)}')
        t = alvo.add_table(rows=1, cols=len(colunas))
        tblPr = t._tbl.tblPr
        margem = 40 if len(colunas) >= 8 else 80
        look = tblPr.find(qn('w:tblLook'))  # o Word exige esta ordem: tblBorders, tblCellMar, tblLook
        for xml in (f'<w:tblBorders {nsdecls("w")}>' + ''.join(
                        f'<w:{b} w:val="single" w:sz="4" w:space="0" w:color="7F7F7F"/>' for b in
                        ('top', 'left', 'bottom', 'right', 'insideH', 'insideV')) + '</w:tblBorders>',
                    f'<w:tblCellMar {nsdecls("w")}><w:left w:w="{margem}" w:type="dxa"/><w:right w:w="{margem}" w:type="dxa"/></w:tblCellMar>'):
            el = parse_xml(xml)
            look.addprevious(el) if look is not None else tblPr.append(el)
        total = largura_total or self.largura
        pesos = larguras or [max(6, min(40, max([len(str(c))] + [len(str(l[i])) for l in linhas[:30]]))) for i, c in enumerate(colunas)]
        soma = float(sum(pesos))
        tam = 8 if len(colunas) >= 8 else 9 if len(colunas) >= 6 else 10
        for i, c in enumerate(colunas):
            cel = t.rows[0].cells[i]
            cel._tc.get_or_add_tcPr().append(parse_xml(f'<w:shd {nsdecls("w")} w:val="clear" w:color="auto" w:fill="E7E6E6"/>'))
            self.runs(cel.paragraphs[0], c, negrito=True, tamanho=tam)
        t.rows[0]._tr.get_or_add_trPr().append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
        for l in linhas:
            cels = t.add_row().cells
            for i, v in enumerate(l):
                self.runs(cels[i].paragraphs[0], '' if v is None else v, amarelo, tamanho=tam)
        t.autofit = False
        for i, p in enumerate(pesos):
            t.columns[i].width = int(total * p / soma)  # tblGrid: o LibreOffice e o Word respeitam
            for cel in t.columns[i].cells:
                cel.width = int(total * p / soma)
        return t

    def codigo(self, alvo, texto, amarelo=False):
        linhas = mascarar(str(texto)).rstrip().split('\n')
        p = alvo.add_paragraph(style=self._estilo('Normal'))
        ppr = p._p.get_or_add_pPr()
        ppr.append(parse_xml(f'<w:shd {nsdecls("w")} w:val="clear" w:color="auto" w:fill="F2F2F2"/>'))
        ppr.append(parse_xml(f'<w:spacing {nsdecls("w")} w:before="60" w:after="60" w:line="240" w:lineRule="auto"/>'))
        ppr.append(parse_xml(f'<w:jc {nsdecls("w")} w:val="left"/>'))
        for i, linha in enumerate(linhas):
            r = p.add_run(linha)
            r.font.name = 'Consolas'; r.font.size = Pt(8.5)
            if amarelo:
                r.font.highlight_color = WD_COLOR_INDEX.YELLOW
            if i < len(linhas) - 1:
                r.add_break()

    def imagem(self, alvo, arquivo, legenda='', largura_cm=None, amarelo=False):
        if not os.path.isfile(arquivo):
            raise ErroConteudo(f'imagem não encontrada: {arquivo}')
        p = alvo.add_paragraph(style=self._estilo('Normal'))
        p.alignment = 1
        maxima = self.largura if not isinstance(alvo, _Cell) else self.largura - Cm(1.1)
        from PIL import Image
        with Image.open(arquivo) as im:
            proporcao = im.height / im.width
        largura = min(Cm(largura_cm), maxima) if largura_cm else maxima
        largura = min(largura, int(Cm(19) / proporcao))  # nunca mais alta que a página
        p.add_run().add_picture(arquivo, width=largura)
        if legenda:
            c = alvo.add_paragraph(style=self._estilo('Caption', 'Normal'))
            c.alignment = 1
            self.runs(c, legenda, amarelo, tamanho=9)

    def blocos(self, alvo, blocos, amarelo=False, pasta=''):
        for b in blocos or []:
            if isinstance(b, str):
                b = {'tipo': 'paragrafo', 'texto': b}
            am = amarelo or bool(b.get('revisar'))
            tipo = b.get('tipo', 'paragrafo')
            if tipo == 'paragrafo':
                self.paragrafo(alvo, b.get('texto', ''), am)
            elif tipo == 'subtitulo':
                self.paragrafo(alvo, b.get('texto', ''), am, negrito=True)
            elif tipo == 'lista':
                self.lista(alvo, b.get('itens', []), bool(b.get('numerada')), am)
            elif tipo == 'tabela':
                self.tabela(alvo, b.get('colunas', []), b.get('linhas', []), am, b.get('larguras'),
                            self.largura - Cm(1.1) if isinstance(alvo, _Cell) else None)
                if not isinstance(alvo, _Cell):
                    alvo.add_paragraph(style=self._estilo('Normal'))
            elif tipo == 'codigo':
                self.codigo(alvo, b.get('texto', ''), am)
            elif tipo == 'imagem':
                arq = b.get('arquivo', '')
                self.imagem(alvo, arq if os.path.isabs(arq) else os.path.join(pasta, arq), b.get('legenda', ''), b.get('largura_cm'), am)
            elif tipo == 'diagrama':
                from . import diagrama
                saida = diagrama.gerar(b['modelo'], os.path.join(pasta, 'diagramas'), self.idioma)
                rot = {'pt-BR': 'diagrama gerado — revisar', 'es': 'diagrama generado — revisar'}[self.idioma]
                self.imagem(alvo, saida['png'], f"{b.get('legenda') or b['modelo'].get('titulo', '')} [[({rot})]]", saida['largura_cm'])
            elif tipo == 'preencher':
                self.paragrafo(alvo, f"[{PREENCHER[self.idioma]}: {b.get('texto', '')}]", True)
            elif tipo == 'quebra_pagina':
                alvo.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
            else:
                raise ErroConteudo(f'tipo de bloco desconhecido: {tipo}')


# ------------------------------------------------------------------ substituições na base
def _paragrafos(doc):
    """Todos os parágrafos: corpo, tabelas (inclusive aninhadas e controles de conteúdo), cabeçalhos e rodapés."""
    partes = [doc.element.body]
    for s in doc.sections:
        for h in (s.header, s.footer, s.first_page_header, s.first_page_footer, s.even_page_header, s.even_page_footer):
            if h is not None and h._element not in partes:
                partes.append(h._element)
    for parte in partes:
        for p in parte.iter(qn('w:p')):
            yield Paragraph(p, doc)


def _texto(par):
    return ''.join(t.text or '' for t in par._p.iter(qn('w:t')))


def substituir(par, antigo, novo, amarelo=False):
    """Troca um trecho preservando a formatação do primeiro run que o contém."""
    ts = list(par._p.iter(qn('w:t')))
    completo = ''.join(t.text or '' for t in ts)
    if antigo not in completo:
        return False
    alvo = next((t for t in ts if antigo in (t.text or '')), None)
    if alvo is not None:
        alvo.text = (alvo.text or '').replace(antigo, novo)
    else:  # trecho espalhado em vários runs: junta tudo no primeiro
        alvo = ts[0]
        alvo.text = completo.replace(antigo, novo)
        for t in ts[1:]:
            t.text = ''
    alvo.set(qn('xml:space'), 'preserve')
    run = Run(alvo.getparent(), par)
    cor = run._r.rPr.find(qn('w:color')) if run._r.rPr is not None else None
    if cor is not None and (cor.get(qn('w:val')) or '').upper() == 'FF0000':
        run._r.rPr.remove(cor)  # o modelo marca em vermelho o que falta preencher
    if amarelo:
        run.font.highlight_color = WD_COLOR_INDEX.YELLOW  # python-docx insere na ordem que o Word exige
    return True


def _capa(doc, esc, pares):
    """pares: [(marcador, valor)]. Valor vazio = fica o marcador, em amarelo."""
    for antigo, novo in pares:
        for par in _paragrafos(doc):
            if antigo in _texto(par):
                if novo:
                    substituir(par, antigo, mascarar(str(novo)))
                else:
                    substituir(par, antigo, antigo, amarelo=True); esc.amarelos += 1


# ------------------------------------------------------------------ LI e Manual
_CAPA = {
    ('li', 'pt-BR'): [('Nome da Empresa', 'terceiro'), ('(Nome do software e Versão)', 'software'),
                      ('Cliente: XXXXXXXXX', 'cliente', 'Cliente: {}'), ('Nome do projeto: XXXXXXXXX', 'projeto', 'Nome do projeto: {}'),
                      ('Gerente de projetos de implantação Bionexo Tasy: XXXXXXXXX', 'gerente_projeto', 'Gerente de projetos de implantação Bionexo Tasy: {}'),
                      ('Consultor: XXXXXXXXX', 'consultor', 'Consultor: {}'), ('Solicitante/E-mail: Nome / Email', 'solicitante', 'Solicitante/E-mail: {}'),
                      ('Registro ID (Ver 1):', 'registro_id', 'Registro ID (Ver {versao}): {}')],
    ('li', 'es'): [('Nome da Empresa', 'terceiro'), ('Nombre de la Empresa', 'terceiro'), ('(Nome do software e Versão)', 'software'),
                   ('(Nombre del software y Versión)', 'software'),
                   ('Cliente: XXXXXXXXX', 'cliente', 'Cliente: {}'), ('Nombre del proyecto: XXXXXXXXX', 'projeto', 'Nombre del proyecto: {}'),
                   ('Gerente de proyectos de implementación Bionexo Tasy: XXXXXXXXX', 'gerente_projeto', 'Gerente de proyectos de implementación Bionexo Tasy: {}'),
                   ('Consultor: XXXXXXXXX', 'consultor', 'Consultor: {}'), ('Solicitante/Correo: Nombre / Correo', 'solicitante', 'Solicitante/Correo: {}'),
                   ('ID de registro (Ver 1):', 'registro_id', 'ID de registro (Ver {versao}): {}')],
    ('manual', 'pt-BR'): [('(NOME DO MANUAL)', 'titulo'), ('(Nome do Manual)', 'titulo_curto'),
                          ('Código do documento: ########', 'codigo', 'Código do documento: {}'),
                          ('Revisão: 00_', 'revisao', 'Revisão: {}'), ('Rev: 00_', 'revisao', 'Rev: {}')],
    ('manual', 'es'): [('(NOMBRE DEL MANUAL)', 'titulo'), ('(Nombre del Manual)', 'titulo_curto'),
                       ('Código del documento: ########', 'codigo', 'Código del documento: {}'),
                       ('Revisión: 00_', 'revisao', 'Revisión: {}'), ('Rev: 00_', 'revisao', 'Rev: {}')],
}


def _estrutura(tipo, raiz):
    return json.load(open(os.path.join(raiz, 'templates', tipo, 'estrutura.json'), encoding='utf8'))


def validar(conteudo, raiz=None):
    """Confere o conteúdo contra templates/<tipo>/estrutura.json. Devolve {'erros': [...], 'avisos': [...]}."""
    raiz = raiz or raiz_padrao()
    erros, avisos = [], []
    tipo, idioma = conteudo.get('tipo'), conteudo.get('idioma')
    if tipo not in TIPOS:
        return {'erros': [f'"tipo" deve ser um de {TIPOS}'], 'avisos': []}
    if idioma not in IDIOMAS:
        erros.append(f'"idioma" deve ser um de {IDIOMAS} (pergunte ao consultor)')
    est = _estrutura(tipo, raiz)
    if tipo == 'cci':
        campos = conteudo.get('campos') or {}
        for c in ('titulo', 'cliente', 'integracao'):
            if not campos.get(c):
                avisos.append(f'campo "{c}" vazio: sairá em amarelo')
        for chave, validos in (('prioridade', est['valores']['prioridade_cliente']), ('impactara_em', est['valores']['impactara_en'])):
            v = campos.get(chave)
            if v and not any(norm_valor(v) == norm_valor(x) for x in validos):
                erros.append(f'campo "{chave}"="{v}" fora dos valores aceitos: {validos}')
        if not (conteudo.get('solicitacao') and conteudo.get('solucao')):
            erros.append('CCI precisa de "solicitacao" e "solucao" (listas de blocos)')
        if campos.get('esforco') or campos.get('custo_adicional'):
            avisos.append('esforço e custo são do consultor: o agente não estima (ver estrutura.json, seção 4)')
        return {'erros': erros, 'avisos': avisos}
    secoes = conteudo.get('secoes') or []
    if not secoes:
        erros.append('"secoes" vazio')
    ids = [str(s.get('id', '')) for s in secoes]
    for s in est['secoes']:
        sid = str(s['id'])
        if s.get('obrigatoria') and sid not in ('capa', 'aviso') and sid not in ids:
            titulo = s['titulo'] if isinstance(s['titulo'], str) else s['titulo'].get(idioma, '')
            erros.append(f'seção obrigatória ausente: {sid} — {titulo}')
    for i, s in enumerate(secoes):
        if not s.get('titulo'):
            erros.append(f'seção {i + 1} sem "titulo"')
        if not s.get('blocos') and not s.get('secoes'):
            prox = secoes[i + 1] if i + 1 < len(secoes) else None
            if not (prox and int(prox.get('nivel', 1)) > int(s.get('nivel', 1))):
                avisos.append(f'seção "{s.get("titulo")}" sem conteúdo: sairá com [{PREENCHER.get(idioma, "PREENCHER")}]')
    return {'erros': erros, 'avisos': avisos}


def norm_valor(v):
    return re.sub(r'[^a-z0-9]', '', str(v).lower().replace('é', 'e').replace('í', 'i'))


def _secoes(doc, esc, conteudo, pasta):
    tipo = conteudo['tipo']
    cont = [0] * 6
    for s in conteudo['secoes']:
        nivel = max(1, min(int(s.get('nivel', 1)), 6))
        cont[nivel - 1] += 1
        cont[nivel:] = [0] * (6 - nivel)
        titulo = re.sub(r'^\s*\d+(\.\d+)*\.?\s+', '', str(s['titulo']))
        am = bool(s.get('revisar'))
        if tipo == 'manual':  # o modelo EMR 12352 traz o número digitado no título (numeração do Word desligada)
            numero = '.'.join(str(c) for c in cont[:nivel])
            if nivel <= 2:
                if nivel == 1 and cont[0] > 1:
                    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
                p = doc.add_paragraph(style=esc._estilo(f'Heading {nivel}'))
                esc.runs(p, f'{numero} {titulo}', am)
            else:
                esc.paragrafo(doc, f'{numero} {titulo}', am, negrito=True)
        else:  # LI: os estilos de título já numeram sozinhos
            p = doc.add_paragraph(style=esc._estilo(f'Heading {nivel}'))
            esc.runs(p, titulo, am)
        if s.get('blocos'):
            esc.blocos(doc, s['blocos'], am, pasta)
        elif not _tem_filhos(conteudo['secoes'], s):
            esc.paragrafo(doc, f"[{PREENCHER[esc.idioma]}: {s.get('instrucao') or titulo}]", True)


def _tem_filhos(secoes, s):
    i = secoes.index(s)
    return i + 1 < len(secoes) and int(secoes[i + 1].get('nivel', 1)) > int(s.get('nivel', 1))


# ------------------------------------------------------------------ CCI (formulário)
_CCI_SLOTS = ['titulo', 'cci_id', 'prioridade', 'cliente', 'pais', 'projeto', 'gerente_bionexo', 'gerente_cliente', 'data',
              'integracao', 'impacto_testes_vendor', 'impactara_em', 'impacto_go_live', '#solicitacao', '#solucao', '#regras_negocio',
              '#comportamento_esperado', '#comportamento_atual', '#impacto', '#informacao_adicional', 'esforco', 'custo_adicional',
              '#comentarios', 'cliente', 'cargo_aprovador_cliente', 'aprovador_cliente', 'data_aprovacao_cliente',
              'aprovador_bionexo', 'data_aprovacao_bionexo', 'gerente_bionexo', 'data_aprovacao_gerente']
_CCI_MARCA = re.compile(r'^\s*(\[.+\]|<.+>|CCI-<CLIENTE>.*|Elija un elemento\.?|Escolha um item\.?)\s*$', re.S)


def _cci(doc, esc, conteudo, pasta):
    campos = dict(conteudo.get('campos') or {})
    corpo = {'solicitacao': conteudo.get('solicitacao'), 'solucao': conteudo.get('solucao'),
             'regras_negocio': conteudo.get('regras_negocio'), 'comportamento_esperado': conteudo.get('comportamento_esperado'),
             'comportamento_atual': conteudo.get('comportamento_atual'), 'impacto': conteudo.get('impacto'),
             'informacao_adicional': conteudo.get('informacao_adicional'), 'comentarios': conteudo.get('comentarios')}
    marcas = [p for p in Paragraph_iter_corpo(doc) if _CCI_MARCA.match(_texto(p))]
    if len(marcas) != len(_CCI_SLOTS):
        raise ErroConteudo(f'base do CCI mudou: {len(marcas)} marcadores, esperado {len(_CCI_SLOTS)} (regerar as bases)')
    for par, slot in zip(marcas, _CCI_SLOTS):
        if slot.startswith('#'):
            blocos = corpo.get(slot[1:])
            if not blocos:
                substituir(par, _texto(par), _texto(par), amarelo=True); esc.amarelos += 1
                continue
            cel = _Cell(_celula(par), doc)
            antes = list(cel._tc)
            esc.blocos(cel, [blocos] if isinstance(blocos, str) else blocos, pasta=pasta)
            novos = [e for e in cel._tc if e not in antes]
            ancora = par._p
            for e in novos:  # add_* escreve no fim da célula: traz para o lugar do marcador
                ancora.addnext(e); ancora = e
            par._p.getparent().remove(par._p)
        else:
            valor = str(campos.get(slot) or '')
            proposta = valor.startswith('[[') and valor.endswith(']]')  # sugestão da IA: vai em amarelo
            if valor:
                substituir(par, _texto(par), mascarar(valor[2:-2] if proposta else valor), amarelo=proposta)
                esc.amarelos += proposta
            else:
                substituir(par, _texto(par), _texto(par), amarelo=True); esc.amarelos += 1
    # "Solicitado por" não tem marcador no modelo: a célula seguinte fica vazia
    for par in Paragraph_iter_corpo(doc):
        if _texto(par).strip().startswith('Solicitado por'):
            prox = _celula(par).getnext()
            if prox is not None and prox.tag == qn('w:tc'):
                alvo = Paragraph(next(prox.iter(qn('w:p'))), doc)
                valor = campos.get('solicitado_por')
                esc.runs(alvo, valor or f'[{PREENCHER[esc.idioma]}: solicitante]', not valor)
            break


def Paragraph_iter_corpo(doc):
    for p in doc.element.body.iter(qn('w:p')):
        yield Paragraph(p, doc)


def _celula(par):
    e = par._p
    while e is not None and e.tag != qn('w:tc'):
        e = e.getparent()
    if e is None:
        raise ErroConteudo('marcador do CCI fora de célula')
    return e


# ------------------------------------------------------------------ entrada principal
def gerar(conteudo, destino, raiz=None):
    """Gera o .docx. Devolve {'arquivo', 'amarelos', 'avisos'}; levanta ErroConteudo se o conteúdo for inválido."""
    raiz = raiz or raiz_padrao()
    v = validar(conteudo, raiz)
    if v['erros']:
        raise ErroConteudo('conteúdo inválido:\n- ' + '\n- '.join(v['erros']))
    tipo, idioma = conteudo['tipo'], conteudo['idioma']
    doc = Document(os.path.join(raiz, 'templates', tipo, f'base-{idioma}.docx'))
    esc = Escritor(doc, idioma)
    pasta = os.path.dirname(os.path.abspath(destino))
    os.makedirs(pasta, exist_ok=True)
    if tipo == 'cci':
        _cci(doc, esc, conteudo, pasta)
    else:
        capa = dict(conteudo.get('capa') or {})
        capa.setdefault('versao', '1')
        if tipo == 'manual':
            capa.setdefault('titulo_curto', capa.get('titulo', ''))
            capa.setdefault('revisao', '00')
            capa['titulo'] = (capa.get('titulo') or '').upper()
        pares = []
        for item in _CAPA[(tipo, idioma)]:
            marcador, campo = item[0], item[1]
            valor = capa.get(campo)
            pares.append((marcador, item[2].format(valor, versao=capa['versao']) if valor and len(item) > 2 else valor))
        _capa(doc, esc, pares)
        if tipo == 'li':  # classificação: marca só a opção informada
            cl = capa.get('classificacao')
            if cl:
                for par in _paragrafos(doc):
                    t = _texto(par)
                    if '[ X ]' in t and ' – ' in t:
                        opcoes = re.split(r'\[\s*X?\s*\]', t)
                        if len(opcoes) == 4:
                            marcado = [norm_valor(cl) in norm_valor(o) for o in opcoes[1:]]
                            if any(marcado):
                                novo = opcoes[0] + ''.join(('[ X ]' if m else '[  ]') + o for m, o in zip(marcado, opcoes[1:]))
                                substituir(par, t, novo)
        doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
        _secoes(doc, esc, conteudo, pasta)
    # move o sectPr para o fim (add_* já mantém; garantia para bases alteradas à mão)
    corpo = doc.element.body
    sect = corpo.find(qn('w:sectPr'))
    if sect is not None and corpo[-1] is not sect:
        corpo.append(sect)
    doc.core_properties.author = 'Bionexo Tasy'
    if tipo == 'cci':  # no modelo, a célula do gerente de projeto Bionexo Tasy é ligada ao autor do arquivo
        gerente = (conteudo.get('campos') or {}).get('gerente_bionexo')
        doc.core_properties.author = gerente or ('<Gerente de projeto Bionexo Tasy>' if idioma == 'pt-BR' else '<Gerente de Proyecto Bionexo Tasy>')
    doc.core_properties.title = str((conteudo.get('capa') or conteudo.get('campos') or {}).get('titulo', ''))
    doc.save(destino)
    return {'arquivo': destino, 'amarelos': esc.amarelos, 'avisos': v['avisos'], 'aviso_final': AVISO[idioma]}
