"""Extrai do código-fonte do tasy-interfaces (Java) os índices usados pelo agente.

Uso: python extrair_interfaces.py <pasta tasy-interfaces> <pasta de saída>

Gera:
  endpoints.json  endpoint -> tabelas gravadas/lidas, entidades JPA e procedures alcançadas
  entidades.json  tabela -> entidades JPA (módulo, classe, colunas)
Heurística: a ligação endpoint -> tabela segue referências entre classes do mesmo
módulo (Resource -> Service -> Repository -> Entity/SQL) até 6 níveis.
"""
import json, os, re, sys, collections

SRC, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)

STR = re.compile(r'"((?:[^"\\\n]|\\.)*)"')
CLASS = re.compile(r'\b(?:class|interface|enum|record)\s+([A-Z]\w*)')
IDENT = re.compile(r'\b[A-Z]\w+\b')
SQLW = re.compile(r'\b(INSERT\s+INTO|UPDATE|DELETE\s+FROM|MERGE\s+INTO)\s+(?:\w+\.)?([A-Z][A-Z0-9_]{2,})\b', re.I)
SQLR = re.compile(r'\b(?:FROM|JOIN)\s+(?:\w+\.)?([A-Z][A-Z0-9_]{2,})\b', re.I)
PROC = [re.compile(r'\bcall\s+([\w$.]+)\s*\(', re.I), re.compile(r'\bbegin\s+([\w$.]+)\s*\(', re.I),
        re.compile(r'createStoredProcedureQuery\(\s*"([\w$.]+)"')]
TABLE = re.compile(r'@Table\s*\(([^)]*)\)', re.S)
NAME = re.compile(r'name\s*=\s*"([\w$]+)"')
COL = re.compile(r'@(?:Column|JoinColumn)\s*\(([^)]*)\)', re.S)
VERB = re.compile(r'@(GET|POST|PUT|PATCH|DELETE)\b')
PATH = re.compile(r'@Path\s*\(\s*"([^"]*)"\s*\)')
SUMMARY = re.compile(r'summary\s*=\s*"((?:[^"\\]|\\.)*)"')
METHOD = re.compile(r'\b(?:public|protected|private)\s+[^;{}=()]*?\b(\w+)\s*\(')
SQL_NOISE = {'DUAL', 'TABLE', 'THE', 'SET', 'WHERE', 'SELECT', 'VALUES', 'TO', 'SYSDATE'}
COL_PREFIX = ('DT_', 'CD_', 'NR_', 'IE_', 'DS_', 'NM_', 'QT_', 'VL_', 'PR_', 'TX_', 'SG_', 'HR_')

def is_table(n, known):
    # filtra palavras de texto e colunas capturadas pelo regex de SQL
    return n in known or ('_' in n and not n.startswith(COL_PREFIX))

def module_of(path):
    return os.path.relpath(path, SRC).split(os.sep)[0]

files = {}
for root, dirs, fs in os.walk(SRC):
    dirs[:] = [d for d in dirs if d not in ('test', 'build', '.git', '.gradle')]
    for f in fs:
        if f.endswith('.java'):
            p = os.path.join(root, f)
            files[p] = open(p, encoding='utf-8', errors='ignore').read()

# classe -> arquivos, por módulo
by_mod_class = collections.defaultdict(dict)
info = {}
for p, t in files.items():
    mod = module_of(p)
    names = set(CLASS.findall(t))
    for n in names:
        by_mod_class[mod][n] = p
    lits = ' '.join(STR.findall(t))
    lits_u = lits.upper()
    w = {m[1].upper() for m in SQLW.findall(lits)} - SQL_NOISE
    r = {m.upper() for m in SQLR.findall(lits) if '_' in m} - SQL_NOISE - w
    procs = set()
    for rx in PROC:
        procs |= {x.upper() for x in rx.findall(lits if rx is not PROC[2] else t)}
    ent = None
    if '@Entity' in t:
        m = TABLE.search(t)
        if m and NAME.search(m.group(1)):
            cols = sorted({NAME.search(c).group(1).upper() for c in COL.findall(t) if NAME.search(c)})
            ent = (NAME.search(m.group(1)).group(1).upper(), cols)
    info[p] = dict(mod=mod, names=names, w=w, r=r, procs=procs, ent=ent,
                   refs=set(IDENT.findall(re.sub(r'"(?:[^"\\\n]|\\.)*"', '', t))) - names)

known = {i['ent'][0] for i in info.values() if i['ent']}
for i in info.values():
    i['w'] = {n for n in i['w'] if is_table(n, known)}
    i['r'] = {n for n in i['r'] if is_table(n, known)}

def reach(p, depth=6):
    mod = info[p]['mod']; seen = {p}; frontier = [p]
    for _ in range(depth):
        nxt = []
        for q in frontier:
            for n in info[q]['refs']:
                r = by_mod_class[mod].get(n)
                if r and r not in seen:
                    seen.add(r); nxt.append(r)
        frontier = nxt
    return seen

endpoints = []
for p, t in files.items():
    if '@Path' not in t or not VERB.search(t):
        continue
    cm = CLASS.search(t)
    if not cm:
        continue
    head = t[:cm.start()]
    base = (PATH.findall(head) or [''])[-1]
    rs = reach(p)
    w = set().union(*(info[q]['w'] for q in rs)); r = set().union(*(info[q]['r'] for q in rs)) - w
    procs = set().union(*(info[q]['procs'] for q in rs))
    ents = {info[q]['ent'][0] for q in rs if info[q]['ent']}
    for vm in VERB.finditer(t, cm.end()):
        mm = METHOD.search(t, vm.end())
        win = t[vm.start():mm.end() if mm else vm.end() + 3000]
        # @Path do método pode vir antes do verbo
        pre = t[max(cm.end(), vm.start() - 400):vm.start()]
        pre = pre[pre.rfind(';') + 1:] if ';' in pre else pre
        pre = pre[pre.rfind('}') + 1:] if '}' in pre else pre
        sub = (PATH.findall(win) or PATH.findall(pre) or [''])[0]
        s = SUMMARY.search(win)
        endpoints.append(dict(
            modulo=info[p]['mod'], metodo=vm.group(1),
            path=('/' + '/'.join(x.strip('/') for x in (base, sub) if x.strip('/'))) or '/',
            classe=cm.group(1), operacao=mm.group(1) if mm else None,
            resumo=s.group(1) if s else None,
            tabelas_escrita_sql=sorted(w), tabelas_leitura_sql=sorted(r),
            entidades_jpa=sorted(ents), procedures=sorted(procs)))

entidades = collections.defaultdict(list)
for p, i in info.items():
    if i['ent']:
        entidades[i['ent'][0]].append(dict(modulo=i['mod'], classe=os.path.basename(p)[:-5], colunas=i['ent'][1]))

endpoints.sort(key=lambda e: (e['modulo'], e['path'], e['metodo']))
json.dump(endpoints, open(os.path.join(OUT, 'endpoints.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(dict(sorted(entidades.items())), open(os.path.join(OUT, 'entidades.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f"arquivos={len(files)} endpoints={len(endpoints)} tabelas_jpa={len(entidades)}")
