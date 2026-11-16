"""Gera as bases .docx limpas (uma por tipo e idioma) a partir dos templates oficiais.

Uso: python gerar_bases_docx.py <pasta templates>
- LI e Manual: mantém capa, sumário e identificação; remove o corpo (o gerador monta o corpo a partir de estrutura.json).
- CCI: mantém o formulário inteiro, troca os valores do exemplo por marcadores e o texto por instruções.
- Traduz os textos fixos parágrafo a parágrafo; parágrafos com campos (página, sumário) só têm palavras trocadas.
- Liga 'atualizar campos ao abrir' para o sumário se refazer no Word.
"""
import html, os, re, sys, zipfile

T = re.compile(r'(<w:t(?:\s[^>]*)?>)([^<]*)(</w:t>)')
P = re.compile(r'<w:p[ >].*?</w:p>|<w:p/>', re.S)

def ptext(p):
    return ''.join(html.unescape(m.group(2)) for m in T.finditer(p)).strip()

def set_text(p, new):
    ms = list(T.finditer(p))
    if not ms:
        return p
    out, last = [], 0
    for i, m in enumerate(ms):
        out.append(p[last:m.start()])
        tag = m.group(1)
        if i == 0 and 'xml:space' not in tag:
            tag = tag.replace('<w:t', '<w:t xml:space="preserve"', 1)
        out += [tag, html.escape(new, quote=False) if i == 0 else '', m.group(3)]
        last = m.end()
    return ''.join(out) + p[last:]

def translate_xml(x, frases, tokens):
    def fix(m):
        p = m.group(0)
        if 'w:fldChar' in p or 'w:fldSimple' in p or 'w:instrText' in p:
            return T.sub(lambda t: t.group(1) + html.escape(_tok(html.unescape(t.group(2)), tokens), quote=False) + t.group(3), p)
        t = ptext(p)
        if t in frases:
            return '' if frases[t] is None else set_text(p, frases[t])
        return p
    return P.sub(fix, x)

def _tok(s, tokens):
    for a, b in tokens:
        s = s.replace(a, b)
    return s

def body_children(x):
    """Spans (ini, fim) dos filhos diretos de <w:body>."""
    b0 = x.index('<w:body>') + len('<w:body>'); b1 = x.rindex('</w:body>')
    spans, depth, i, start = [], 0, b0, None
    tag = re.compile(r'<(/?)(w:[A-Za-z]+)([^>]*?)(/?)>')
    for m in tag.finditer(x, b0, b1):
        closing, selfc = m.group(1) == '/', m.group(4) == '/'
        if not closing and depth == 0:
            start = m.start()
        if closing:
            depth -= 1
        elif not selfc:
            depth += 1
        if depth == 0 and start is not None:
            spans.append((start, m.end())); start = None
    return b0, b1, spans

def reset_toc(x, aviso):
    """Troca as entradas em cache do sumário por um campo TOC vazio (o Word refaz ao abrir)."""
    ps = list(P.finditer(x)); start = None
    for i, m in enumerate(ps):
        if re.search(r'<w:instrText[^>]*>\s*TOC\b', m.group(0)):
            start = i; break
    if start is None:
        return x
    instr = re.search(r'<w:instrText[^>]*>([^<]*TOC[^<]*)</w:instrText>', ps[start].group(0)).group(1)
    depth, end = 0, start
    for j in range(start, len(ps)):
        for t in re.findall(r'w:fldCharType="(begin|end)"', ps[j].group(0)):
            depth += 1 if t == 'begin' else -1
        if depth <= 0:
            end = j; break
    novo = ('<w:p><w:r><w:fldChar w:fldCharType="begin"/></w:r><w:r><w:instrText xml:space="preserve">%s</w:instrText></w:r>'
            '<w:r><w:fldChar w:fldCharType="separate"/></w:r><w:r><w:t>%s</w:t></w:r><w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>') % (instr, aviso)
    return x[:ps[start].start()] + novo + x[ps[end].end():]

LOGO_XML = ('<w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="{cx}" cy="{cy}"/>'
    '<wp:docPr id="9001" name="Logo Bionexo Tasy"/><a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
    '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
    '<pic:nvPicPr><pic:cNvPr id="0" name="logo-bionexo-tasy.png"/><pic:cNvPicPr/></pic:nvPicPr><pic:blipFill><a:blip r:embed="rIdLogo"/>'
    '<a:stretch><a:fillRect/></a:stretch></pic:blipFill><pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
    '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r>')

def logo_png(base):
    # mesmo logo do cabeçalho da CCI/EMR 0198 (md5 632a8f2b...), evita versionar outro arquivo
    return zipfile.ZipFile(os.path.join(base, 'cci', 'CCI Template Control de cambios integraciones_Bionexo_Tasy.docx')).read('word/media/image1.png')

def put_logo(hdr):
    # célula 1 do cabeçalho da LI oficial é o espaço do logo e veio vazia
    i = hdr.index('<w:tc>'); j = hdr.index('</w:pPr></w:p>', i) + len('</w:pPr>')
    assert not re.search(r'<w:t[ >]', hdr[i:j]), 'célula do logo não está vazia'
    return hdr[:j] + LOGO_XML.format(cx=914400, cy=161600) + hdr[j:]

def build(src, dst, frases, tokens, keep_until=None, toc=None, logo=None, ajustes=()):
    zin = zipfile.ZipFile(src); zout = zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED)
    if logo:
        assert 'word/_rels/header1.xml.rels' not in zin.namelist()
        zout.writestr('word/_rels/header1.xml.rels', '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rIdLogo" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/logo-bionexo-tasy.png"/></Relationships>')
        zout.writestr('word/media/logo-bionexo-tasy.png', logo)
    for it in zin.infolist():
        d = zin.read(it.filename)
        if re.match(r'word/(document|header\d+|footer\d+)\.xml$', it.filename):
            x = d.decode('utf8')
            if it.filename == 'word/document.xml' and keep_until is not None:
                b0, b1, sp = body_children(x)
                keep = [x[a:b] for i, (a, b) in enumerate(sp) if i <= keep_until or x[a:b].startswith('<w:sectPr')]
                x = x[:b0] + ''.join(keep) + x[b1:]
            x = translate_xml(x, frases, tokens)
            x = re.sub(r'<w:tblCaption w:val="[^"]*"/>', '', x)  # legenda de teste esquecida no template
            for padrao, novo in (ajustes if it.filename == 'word/document.xml' else ()):
                x, n = re.subn(padrao, novo, x)
                assert n, f'ajuste sem efeito: {padrao}'
            if logo and it.filename == 'word/header1.xml':
                x = put_logo(x)
            if it.filename == 'word/document.xml' and toc:
                x = reset_toc(x, toc)
            d = x.encode('utf8')
        elif it.filename == 'word/settings.xml':
            s = d.decode('utf8')
            if 'w:updateFields' not in s:
                # ordem do schema: updateFields vem antes destes elementos (senão o Word pode acusar erro)
                depois = re.search(r'<w:(hdrShapeDefaults|footnotePr|endnotePr|compat|docVars|rsids|m:mathPr|themeFontLang|clrSchemeMapping|shapeDefaults|decimalSymbol|listSeparator)\b|<m:mathPr|</w:settings>', s)
                s = s[:depois.start()] + '<w:updateFields w:val="true"/>' + s[depois.start():]
            d = s.encode('utf8')
        elif it.filename == 'docProps/core.xml':
            d = re.sub(rb'<dc:creator>.*?</dc:creator>', b'<dc:creator>Bionexo Tasy</dc:creator>', d)
            d = re.sub(rb'<cp:lastModifiedBy>.*?</cp:lastModifiedBy>', b'<cp:lastModifiedBy>Bionexo Tasy</cp:lastModifiedBy>', d)
        zout.writestr(it, d)
    zout.close()
    zipfile.ZipFile(dst).testzip()
    print('ok', dst)

# ---------------- LI (base oficial PT) ----------------
LI_PT = {'Gerente de projetos de implantação Philips: XXXXXXXXX': 'Gerente de projetos de implantação Bionexo Tasy: XXXXXXXXX'}
LI_ES = {
 'Documento de especificação de requisito e processos da integração': 'Documento de especificación de requerimiento y procesos de integración',
 'Documento de Especificação de requisito e processos de integração': 'Documento de especificación de requerimiento y procesos de integración',
 'Nome da Empresa': 'Nombre de la Empresa', '(Nome do software e Versão)': '(Nombre del software y versión)',
 'Conteúdo': 'Índice', 'Cliente: XXXXXXXXX': 'Cliente: XXXXXXXXX', 'Nome do projeto: XXXXXXXXX': 'Nombre del proyecto: XXXXXXXXX',
 'Gerente de projetos de implantação Philips: XXXXXXXXX': 'Gerente de proyectos de implementación Bionexo Tasy: XXXXXXXXX',
 'Consultor: XXXXXXXXX': 'Consultor: XXXXXXXXX', 'Solicitante/E-mail: Nome / Email': 'Solicitante/Correo: Nombre / Correo',
 'Classificação: [ X ] Novo processo – [  ] Alteração – [  ] Correções -': 'Clasificación: [ X ] Nuevo proceso – [  ] Cambios – [  ] Correcciones -',
 'Registro ID (Ver 1):': 'ID de registro (Ver 1):'}
TOK_PT_LI = [('Page', 'Página'), (' of ', ' de ')]
TOK_ES = TOK_PT_LI + [('Conteúdo', 'Índice')]

# ---------------- Manual (base oficial ES) ----------------
MO_PT = {
 '(NOMBRE DEL MANUAL)': '(NOME DO MANUAL)', 'ADVERTENCIA': 'AVISO',
 'El contenido de este documento es propiedad exclusiva de Bionexo Tasy y esta sujeta a cambios sin previo aviso.': 'O conteúdo deste documento é propriedade exclusiva da Bionexo Tasy e está sujeito a alterações sem aviso prévio.',
 'Esta copia deberá ser protegida contra la divulgación no autorizada, como la copia de la documentación electrónica, impresa o parte de ella, no deberá ser prestada, reproducida o vendida.': 'Esta cópia deverá ser protegida contra a divulgação não autorizada; a documentação eletrônica, impressa ou parte dela não deverá ser emprestada, reproduzida ou vendida.',
 'Todos los nombres de empresas, productos, marcas comerciales, personas, personajes, datos o situaciones citadas en este documento son ficticios y tienen fines únicamente educativos.': 'Todos os nomes de empresas, produtos, marcas comerciais, pessoas, personagens, dados ou situações citados neste documento são fictícios e têm fins exclusivamente educativos.',
 '2 Resumen': 'Sumário', 'Manual de Integración': 'Manual de Integração', 'Código del documento: ########': 'Código do documento: ########',
 '(Nombre del Manual)': '(Nome do Manual)', 'Revisión: 00_': 'Revisão: 00_', 'Status: Aprobado': 'Status: Aprovado', 'COPIAS NO CONTROLADAS': 'CÓPIAS NÃO CONTROLADAS'}
MO_ES = {'2 Resumen': 'Resumen'}
TOK_PT_MO = [('Confidencial de la Empresa', 'Confidencial da Empresa'), ('Página', 'Página'), (' de ', ' de ')]

# ---------------- CCI (base oficial ES, preenchida com exemplo) ----------------
CCI_VAL_ES = {
 'BackOffice Finanzas: Ajuste en lógica de obtención de código de deudor/acreedor con base en la persona de la nota fiscal': '[Título del cambio]',
 '1 - Alta': 'Elija un elemento.', 'México': '<País>', 'Proyecto integraciones Interface <Cliente>': '<Nombre del proyecto>',
 '22 abr. 26': '<DD/MMM/AAAA>', 'Backoffice Finanzas': '<Integración>', 'Si': 'Elija un elemento.', '1- TIE': 'Elija un elemento.',
 '1 - Alta (>60hrs)': 'Elija un elemento.', 'No': 'Elija un elemento.', 'Director de TI': '<Cargo>',
 'Actualmente, la integración de BackOffice Finanzas utiliza distintas reglas para determinar el código de deudor enviado al SAP, dependiendo del tipo de documento o escenario procesado.': '[Describir el contexto, la necesidad del cliente, la situación actual y las decisiones tomadas en la sesión (con fecha). Registrar condicionantes.]',
 'Se requiere ajustar la lógica de integración de BackOffice Finanzas para que la obtención del código de deudor o acreedor enviado al SAP sea realizada siempre con base en la persona definida en la nota fiscal, sin considerar como criterio principal al paciente, al registro del anticipo o al convenio de forma aislada.': '[Describir la solución propuesta y lo que contempla el cambio.]',
 'Siempre que la integración requiera enviar un deudor o acreedor al SAP, éste deberá obtenerse con base en la persona registrada en la nota fiscal.': '[Reglas de negocio del cambio.]',
 'El código de deudor o acreedor enviado al SAP debe corresponder siempre a la persona registrada en la nota fiscal.': '[Comportamiento esperado después del cambio.]',
 'En anticipos, se utiliza la persona del anticipo como deudor.': '[Comportamiento actual.]',
 'Posibles inconsistencias entre la información fiscal de la nota y la información contable integrada al SAP.': '[Impactos identificados.]',
 'Confirmación por parte del equipo SAP sobre el tratamiento esperado cuando la persona de la nota fiscal sea distinta del paciente o del convenio.': '[Evidencias del análisis y pendientes de confirmación.]',
 'Este ajuste modifica una regla central de determinación de terceros en la integración.': '[Comentarios adicionales.]'}
for t in ['En la lógica actual:', 'El cambio contempla lo siguiente:', 'Este ajuste implica modificaciones en la lógica de obtención, clasificación y mapeo de terceros enviados desde TASY hacia SAP a través del TIE.',
          'La persona considerada podrá ser física o moral, conforme a la información fiscal del documento.', 'No deberá priorizarse automáticamente al paciente, al anticipo o al convenio si éstos no corresponden a la persona facturada en la NF.',
          'La lógica debe aplicarse de forma uniforme para todos los documentos integrados.', 'Debe existir consistencia entre el emisor/receptor fiscal del documento y el tercero contable enviado al SAP.',
          'En cuenta paciente particular, se utiliza el código del paciente como deudor.', 'En cuenta paciente de convenio, se utiliza el deudor del convenio.',
          'La lógica actual no siempre corresponde con la persona registrada en la nota fiscal.', 'Riesgo de enviar terceros incorrectos en documentos financieros.',
          'Afectación en la trazabilidad y conciliación contable.', 'teste']:
    CCI_VAL_ES[t] = None
def _rm_prefix(prefixes):
    return prefixes
CCI_RM_PREFIX = ['Para anticipos, se envía', 'Para cuenta paciente particular', 'Para cuenta paciente de convenio', 'Esta lógica provoca que', 'Por lo tanto, se identificó',
                 'Obtener el código de deudor', 'Considerar como fuente de referencia', 'Aplicar esta lógica de forma consistente', 'Sustituir la lógica actual', 'Mantener alineación entre']
CCI_PT_LABELS = {
 'Solicitud de cambio - Informaciones': 'Solicitação de mudança - Informações', 'CCI Titulo:': 'Título do CCI:', 'CCI ID:': 'ID do CCI:',
 'Prioridad Cliente:': 'Prioridade do cliente:', 'Nombre del Proyecto:': 'Nome do projeto:', 'Gerente de Proyecto Bionexo Tasy:': 'Gerente de projeto Bionexo Tasy:',
 'Gerente de Proyecto Cliente:': 'Gerente de projeto cliente:', 'Fecha:': 'Data:', 'Integración:': 'Integração:', '¿Impacto pruebas vendor?': 'Impacto nos testes do fornecedor?',
 'Cambio impactará en:': 'Mudança impactará em:', '¿Impacto Go Live?': 'Impacto no Go Live?', 'Solicitud de cambio': 'Solicitação de mudança',
 'Solución Propuesta': 'Solução proposta', 'Reglas de Negocio': 'Regras de negócio', 'Comportamiento Esperado': 'Comportamento esperado',
 'Comportamiento Actual': 'Comportamento atual', 'Información Adicional Requerida': 'Informação adicional necessária',
 'Resumen de Evaluación de Impacto (Bionexo Tasy)': 'Resumo da avaliação de impacto (Bionexo Tasy)', 'Esfuerzo': 'Esforço', 'Complexidad x horas:': 'Complexidade x horas:',
 'Costo:': 'Custo:', '¿Costo adicional?': 'Custo adicional?', 'Comentarios Adicionales': 'Comentários adicionais', 'Aprobación Cliente': 'Aprovação do cliente',
 '☐Aprobado  ☐ Rechazado': '☐Aprovado  ☐ Rejeitado', 'Si es rechazado, motivo:': 'Se rejeitado, motivo:', 'Aprobado por:': 'Aprovado por:', 'Nombre': 'Nome',
 'Fecha': 'Data', 'Firma': 'Assinatura', 'Aprobación Bionexo Tasy': 'Aprovação Bionexo Tasy', 'Control Cambio Integración': 'Controle de Mudança de Integração',
 '<Gerente de Proyecto Bionexo Tasy>': '<Gerente de projeto Bionexo Tasy>', '<Gerente de Proyecto Cliente>': '<Gerente de projeto cliente>',
 '<Nombre aprobador cliente>': '<Nome do aprovador cliente>', '<Nombre aprobador Bionexo Tasy>': '<Nome do aprovador Bionexo Tasy>'}
PT_VAL = {'[Título del cambio]': '[Título da mudança]', 'Elija un elemento.': 'Escolha um item.', '<Nombre del proyecto>': '<Nome do projeto>', '<Integración>': '<Integração>',
          '[Describir el contexto, la necesidad del cliente, la situación actual y las decisiones tomadas en la sesión (con fecha). Registrar condicionantes.]': '[Descrever o contexto, a necessidade do cliente, a situação atual e as decisões tomadas na sessão (com data). Registrar condicionantes.]',
          '[Describir la solución propuesta y lo que contempla el cambio.]': '[Descrever a solução proposta e o que a mudança contempla.]', '[Reglas de negocio del cambio.]': '[Regras de negócio da mudança.]',
          '[Comportamiento esperado después del cambio.]': '[Comportamento esperado após a mudança.]', '[Comportamiento actual.]': '[Comportamento atual.]',
          '[Impactos identificados.]': '[Impactos identificados.]', '[Evidencias del análisis y pendientes de confirmación.]': '[Evidências da análise e pendências de confirmação.]',
          '[Comentarios adicionales.]': '[Comentários adicionais.]'}
TOK_PT_CCI = [('Page', 'Página'), ('of', 'de')]

def cci_frases(src):
    x = zipfile.ZipFile(src).read('word/document.xml').decode('utf8')
    f = dict(CCI_VAL_ES)
    for p in P.findall(x):
        t = ptext(p)
        if any(t.startswith(pr) for pr in CCI_RM_PREFIX):
            f[t] = None
    return f

if __name__ == '__main__':
    base = sys.argv[1]
    li = os.path.join(base, 'li', 'Template de levantamento de integração [OFICIAL].docx')
    mo = os.path.join(base, 'manual', 'EMR 12352 MO - Modelo para Manual de Integración_009_ES.docx')
    cci = os.path.join(base, 'cci', 'CCI Template Control de cambios integraciones_Bionexo_Tasy.docx')
    PT, ES = '[Sumário: atualizar campo (F9)]', '[Índice: actualizar campo (F9)]'
    build(li, os.path.join(base, 'li', 'base-pt-BR.docx'), LI_PT, TOK_PT_LI, keep_until=50, toc=PT, logo=logo_png(base))
    build(li, os.path.join(base, 'li', 'base-es.docx'), LI_ES, TOK_ES, keep_until=50, toc=ES, logo=logo_png(base))
    build(mo, os.path.join(base, 'manual', 'base-es.docx'), MO_ES, [], keep_until=59, toc=ES)
    build(mo, os.path.join(base, 'manual', 'base-pt-BR.docx'), MO_PT, TOK_PT_MO, keep_until=59, toc=PT)
    fes = cci_frases(cci)
    # listas suspensas conforme definido pela equipe: só a complexidade Alta tem faixa de horas; inclui "4 - Tasy (Producto)"
    CCI_AJUSTES = [(r'2 - Media \(21 a 60hrs ?\)', '2 - Media'), (r'3 - Baja \(8 a 20Hrs\)', '3 - Baja'),
                   (r'(<w:listItem w:displayText="3 - TIE/IBE" w:value="[^"]*"/>)(?!<w:listItem w:displayText="4)',
                    r'\1<w:listItem w:displayText="4 - Tasy (Producto)" w:value="4 - Tasy (Producto)"/>')]
    build(cci, os.path.join(base, 'cci', 'base-es.docx'), fes, TOK_PT_CCI, ajustes=CCI_AJUSTES)
    tmp = os.path.join(base, 'cci', 'base-es.docx')
    build(tmp, os.path.join(base, 'cci', 'base-pt-BR.docx'), {**CCI_PT_LABELS, **PT_VAL}, TOK_PT_CCI)
