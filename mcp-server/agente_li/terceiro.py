"""Extrai requisitos de um documento de terceiro no padrão "Resumo / Filtros / SQL" (ex.: Evya 4uHub).

Saída: lista de requisitos no formato comum (requisitos.json) que o classificador consome.
Documentos em outro formato são convertidos para o mesmo formato pela IA (skill gerar-li).
"""
import re

TITULO = re.compile(r'^\s*(\d+)\.\s*(.+?)\s*\.{3,}\s*\d+\s*$')
GRUPO = re.compile(r'^Grupo\s+(.+?)\s*\.{3,}\s*\d+\s*$')
SQL_KW = {'select', 'from', 'where', 'and', 'or', 'on', 'join', 'left', 'inner', 'outer', 'set', 'values', 'into',
          'update', 'insert', 'delete', 'not', 'null', 'is', 'in', 'exists', 'case', 'when', 'then', 'else', 'end',
          'as', 'by', 'order', 'group', 'union', 'all', 'distinct', 'nvl', 'decode', 'trunc', 'sysdate', 'to_date',
          'to_char', 'like', 'between', 'with', 'having', 'dual', 'rownum', 'fetch', 'first', 'rows', 'only', 'offset'}


def texto_pdf(caminho):
    """Texto do PDF com o layout preservado (pypdf: puro Python, funciona igual em Windows e macOS)."""
    from pypdf import PdfReader
    paginas = PdfReader(caminho).pages
    texto = '\n'.join((p.extract_text(extraction_mode='layout') or '') for p in paginas)
    if len(texto.strip()) < 50 * len(paginas):
        raise ValueError('PDF sem camada de texto (provável digitalização): a IA deve ler as páginas por visão')
    return texto


def limpar(t):
    t = t.replace('​', '').replace(' ', ' ')
    return re.sub(r'^\s*Página \d+ de \d+\s*$', '', t, flags=re.M)


def sumario(t):
    """Lê o sumário: [(grupo, numero, titulo)] na ordem do documento."""
    itens, grupo = [], None
    for linha in t.splitlines()[:200]:
        g = GRUPO.match(linha)
        if g:
            grupo = g.group(1); continue
        m = TITULO.match(linha)
        if m and grupo:
            itens.append((grupo, int(m.group(1)), m.group(2).strip()))
    return itens


def _ancora(titulo):
    return re.escape(titulo).replace(r'\ ', r'\s*')


def secoes(t):
    itens = sumario(t)
    corpo_ini = t.find('Grupo ' + itens[0][0], t.find(itens[-1][2]) + 1)
    pos, achados = corpo_ini, []
    for grupo, n, tit in itens:
        m = re.compile(r'^\s*%d\.\s*%s\s*$' % (n, _ancora(tit)), re.M).search(t, pos)
        if not m:
            raise ValueError(f'título não encontrado no corpo: {n}. {tit}')
        achados.append((grupo, n, tit, m.start(), m.end()))
        pos = m.end()
    out = []
    for i, (grupo, n, tit, a, b) in enumerate(achados):
        fim = achados[i + 1][3] if i + 1 < len(achados) else len(t)
        bloco = t[b:fim]
        bloco = re.split(r'^Grupo\s+\S', bloco, flags=re.M)[0]
        out.append((grupo, n, tit, bloco))
    return out


def _parte(bloco, ini, fims):
    m = re.search(ini, bloco)
    if not m:
        return ''
    resto = bloco[m.end():]
    cortes = [x.start() for f in fims for x in [re.search(f, resto)] if x]
    return resto[:min(cortes)] if cortes else resto


def analisar_sql(sql):
    """Tabelas lidas/gravadas, procedures chamadas e colunas (TABELA.COLUNA) no schema do Tasy ({database})."""
    low = re.sub(r'--[^\n]*', ' ', sql).lower()
    tabelas, chamadas = set(), set()
    for m in re.finditer(r'\{database\}\.([a-z_][\w$]*(?:\.[a-z_][\w$]*)?)', low):
        nome = m.group(1).upper()
        (chamadas if low[m.end():].lstrip().startswith('(') else tabelas).add(nome)
    procedures = sorted({x.upper() for x in re.findall(r'(?:\bbegin|;)\s*\{database\}\.([a-z_][\w$.]*)\s*\(', low)})
    funcoes = sorted(chamadas - set(procedures))
    alias = {t.lower(): t for t in tabelas}
    for tab, al in re.findall(r'\{database\}\.([a-z_][\w$]*)\s+([a-z_]\w*)', low):
        if al not in SQL_KW and tab.upper() in tabelas:
            alias[al] = tab.upper()
    escrita = {}
    for op, t in re.findall(r'\b(insert\s+into|update|delete\s+from|merge\s+into)\s+\{database\}\.([a-z_]\w*)', low):
        escrita[t.upper()] = op.split()[0].upper()
    colunas = set()
    for al, col in re.findall(r'\b([a-z_]\w*)\.([a-z_]\w*)\b', low):
        if al in alias and col not in SQL_KW:
            colunas.add(f'{alias[al]}.{col.upper()}')
    for tab, corpo in re.findall(r'\bupdate\s+\{database\}\.([a-z_]\w*)(?:\s+\w+)?\s+set\s+(.+?)\bwhere\b', low, re.S):
        for col in re.findall(r'(?:^|,)\s*(?:\w+\.)?([a-z_]\w*)\s*=', corpo):
            colunas.add(f'{tab.upper()}.{col.upper()}')
    for tab, cols in re.findall(r'insert\s+into\s+\{database\}\.([a-z_]\w*)\s*\(([^)]*)\)', low, re.S):
        for col in re.findall(r'[a-z_]\w*', cols):
            colunas.add(f'{tab.upper()}.{col.upper()}')
    # principal: a gravada; senão a mais citada em colunas (o 1º FROM costuma ser subquery de apoio)
    cont = {}
    for c in colunas:
        cont[c.split('.')[0]] = cont.get(c.split('.')[0], 0) + 1
    principal = next(iter(escrita), None) or (max(cont, key=cont.get) if cont else None)
    return {'tabela_principal': principal, 'tabelas_escrita': escrita, 'procedures': procedures,
            'tabelas_leitura': sorted(tabelas - set(escrita)), 'colunas': sorted(colunas), 'funcoes': funcoes}


def extrair(caminho_pdf):
    t = limpar(texto_pdf(caminho_pdf))
    reqs = []
    for grupo, n, tit, bloco in secoes(t):
        resumo = ' '.join(_parte(bloco, r'Resumo:', [r'\n\s*Filtros:', r'\n\s*SQL']).split())
        filtros = ' '.join(_parte(bloco, r'Filtros:', [r'\n\s*SQL']).split())
        sql = _parte(bloco, r'SQL[^\n]*:', [r'\n\s*(?:Observa|Nota)[^\n]*:'])
        info = analisar_sql(sql)
        m = re.search(r'\[(GET|POST|PUT|PATCH|DELETE)\]|\((GET|POST|PUT|PATCH|DELETE)\)|,\s*(GET|POST|PUT|PATCH|DELETE)\]', tit)
        metodo = next((g for g in m.groups() if g), None) if m else None
        if not metodo:
            metodo = 'POST' if 'INSERT' in info['tabelas_escrita'].values() else 'PUT' if info['tabelas_escrita'] or info['procedures'] else 'GET'
        nome = re.sub(r'\s*[\[(].*$', '', tit).split('.')[-1].strip()
        reqs.append({'id': f'{grupo}#{n}', 'grupo': grupo, 'numero': n, 'titulo': tit, 'nome': nome,
                     'metodo': metodo, 'operacao': 'escrita' if info['tabelas_escrita'] or info['procedures'] else 'leitura',  # POST de busca (ex.: Bot) é leitura
                     'resumo': resumo, 'filtros': filtros, **info})
    return reqs
