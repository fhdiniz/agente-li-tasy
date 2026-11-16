"""Extrai do repositório PL/SQL do Tasy os índices usados pelo agente.

Uso: python extrair_plsql.py <pasta emr-tasy-plsql> <pasta de saída> [tabelas_extra.json ...]

Gera:
  objetos.jsonl          um objeto por linha: schema, tipo, nome, assinatura, descrição,
                         tabelas gravadas/lidas, eventos TIE disparados, tabela do trigger
  tabelas_escrita.json   tabela -> objetos PL/SQL que gravam nela (INSERT/UPDATE/DELETE/MERGE)
  eventos_tie.json       evento TIE (call_bifrost_content) -> objetos que disparam, tabela e payload
  agend_integracao.json  código de gravar_agend_integracao -> objetos que disparam (integrações HL7 legadas)
Não copia o corpo dos objetos: só assinatura e metadados.
"""
import json, os, re, sys, collections

SRC, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
EXT = {'.prc': 'procedure', '.fnc': 'function', '.trg': 'trigger', '.vw': 'view', '.pck': 'package', '.pkb': 'package body', '.pks': 'package'}

COMMENT = re.compile(r'/\*.*?\*/|--[^\n]*', re.S)
STRLIT = re.compile(r"'(?:[^']|'')*'")
NAME = re.compile(r'create\s+(?:or\s+replace\s+)?(?:editionable\s+|noneditionable\s+)?(function|procedure|trigger|view|package\s+body|package|type\s+body|type)\s+(?:"?\w+"?\.)?"?([\w$#]+)"?', re.I)
SIG_END = re.compile(r'\b(is|as)\b', re.I)
W = re.compile(r'\b(?:insert\s+into|update|delete\s+from|delete|merge\s+into)\s+(?:\w+\.)?([a-z][\w$#]*)', re.I)
R = re.compile(r'\b(?:from|join)\s+(?:\w+\.)?([a-z][\w$#]*)', re.I)
TRIG = re.compile(r'\b(?:before|after|instead\s+of)\s+[\w\s,]*?\bon\s+(?:\w+\.)?([a-z][\w$#]*)', re.I)
BIFROST = re.compile(r"\b(?:call_bifrost_content|execute_bifrost_integration)\s*\(\s*'([\w.\-]+)'\s*(?:,\s*'([^']*)')?", re.I)
AGEND = re.compile(r'\bgravar_agend_integracao\s*\(\s*(\d+)', re.I)
KW = {'DUAL', 'TABLE', 'THE', 'SET', 'WHERE', 'SELECT', 'VALUES', 'TO', 'SYSDATE', 'WHEN', 'THEN', 'ELSE', 'END', 'IN', 'AND', 'OR',
      'NOT', 'NULL', 'CURSOR', 'LOOP', 'BEGIN', 'RETURN', 'INTO', 'OF', 'ON', 'FOR', 'IS', 'AS', 'BY', 'CASE', 'EXISTS', 'ALL', 'ANY'}

def clean(n):
    n = n.upper()
    if n in KW or n.endswith(('_W', '_P')) or re.fullmatch(r'C\d+|[A-Z]\d*', n) or n.startswith(('V_', 'W_', 'P_')):
        return None
    return n

objs = []
for root, dirs, fs in os.walk(os.path.join(SRC, 'objects')):
    for f in fs:
        ext = os.path.splitext(f)[1].lower()
        if ext not in EXT:
            continue
        p = os.path.join(root, f)
        raw = open(p, encoding='latin-1').read()
        rel = os.path.relpath(p, SRC)
        schema = rel.split(os.sep)[1]
        m = NAME.search(raw)
        typ = (m.group(1).lower() if m else EXT[ext]); name = (m.group(2) if m else os.path.splitext(f)[0]).upper()
        head_comment = ' '.join(c.strip('/*- \n') for c in COMMENT.findall(raw[: (m.start() if m else 0) + 2000])[:2])
        body = COMMENT.sub(' ', raw)
        events = [(e.lower(), pl) for e, pl in BIFROST.findall(body)]
        agend = sorted({int(x) for x in AGEND.findall(body)})
        nolit = STRLIT.sub("''", body)
        sig = None
        if m and typ in ('function', 'procedure'):
            se = SIG_END.search(nolit, m.end())
            sig = re.sub(r'\s+', ' ', nolit[m.start(): se.start() if se else m.end() + 400]).strip()[:600]
        trig = TRIG.search(nolit) if typ == 'trigger' else None
        objs.append(dict(s=schema, t=typ, n=name, f=rel.replace(os.sep, '/'), sig=sig,
                         desc=re.sub(r'\s+', ' ', head_comment).strip()[:300] or None,
                         w=sorted({c for c in map(clean, W.findall(nolit)) if c}),
                         r=sorted({c for c in map(clean, R.findall(nolit)) if c}),
                         on=trig.group(1).upper() if trig else None, ev=events, ag=agend))

# universo de tabelas: gravadas por algum objeto + tabelas de trigger + extras (JPA, Swagger)
known = {t for o in objs for t in o['w']} | {o['on'] for o in objs if o['on']}
for extra in sys.argv[3:]:
    known |= set(json.load(open(extra, encoding='utf-8')))
names = {o['n'] for o in objs}
for o in objs:
    o['r'] = [t for t in o['r'] if t in known and t not in o['w']]
    o['w'] = [t for t in o['w'] if t not in names]  # descarta falsos positivos que são nomes de objetos

with open(os.path.join(OUT, 'objetos.jsonl'), 'w', encoding='utf-8') as fo:
    for o in sorted(objs, key=lambda o: (o['s'], o['t'], o['n'])):
        fo.write(json.dumps({k: v for k, v in o.items() if v}, ensure_ascii=False) + '\n')

esc = collections.defaultdict(list); ev = collections.defaultdict(list); ag = collections.defaultdict(list)
for o in objs:
    ref = f"{o['s']}.{o['n']} ({o['t']})"
    for t in o['w']: esc[t].append(ref)
    for e, pl in o['ev']: ev[e].append(dict(objeto=ref, tabela_trigger=o['on'], payload=pl or None))
    for c in o['ag']: ag[str(c)].append(dict(objeto=ref, tabela_trigger=o['on']))
dump = lambda d, n: json.dump(d, open(os.path.join(OUT, n), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
dump({k: sorted(v) for k, v in sorted(esc.items())}, 'tabelas_escrita.json')
dump(dict(sorted(ev.items())), 'eventos_tie.json')
dump(dict(sorted(ag.items(), key=lambda x: int(x[0]))), 'agend_integracao.json')
print(f"objetos={len(objs)} tabelas_gravadas={len(esc)} eventos_tie={len(ev)} codigos_agend={len(ag)}")
