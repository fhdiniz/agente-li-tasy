"""Extrai o catálogo de integrações TIE a partir do repositório tie-integrations (.bft).

Uso: python extrair_tie.py <pasta tie-integrations> <pasta de saída>

Gera:
  catalogo.json  um item por arquivo .bft: integrações, eventos (campos), rotas, conectores e fluxos
  apis.json      path de API do Tasy -> integrações que a chamam
  readmes/       README de cada integração (quando existe)
Não extrai credenciais, keystores nem valores padrão de configuração (hosts, senhas).
"""
import json, os, re, sys, glob, collections, shutil

SRC, OUT = sys.argv[1], sys.argv[2]
os.makedirs(os.path.join(OUT, 'readmes'), exist_ok=True)

URI = re.compile(r'<(?:from|to|toD|wireTap|enrich|pollEnrich)\s+uri="([^"]+)"')
APIPATH = re.compile(r'(/(?:tasy-backend/resources/)?api/[\w\-/{}$.\[\]]+)')
SQLW = re.compile(r'\b(INSERT\s+INTO|UPDATE|DELETE\s+FROM|MERGE\s+INTO)\s+(?:\w+\.)?([A-Z][A-Z0-9_]{2,})\b', re.I)
SQLR = re.compile(r'\b(?:FROM|JOIN)\s+(?:\w+\.)?([A-Z][A-Z0-9_]{2,})\b', re.I)
PROC = re.compile(r'\b(?:call|begin|exec)\s+([\w$.]+)\s*\(', re.I)
METHOD = re.compile(r'CamelHttpMethod"?\s*>\s*<constant>\s*(\w+)', re.I)
COL_PREFIX = ('DT_', 'CD_', 'NR_', 'IE_', 'DS_', 'NM_', 'QT_', 'VL_', 'PR_', 'TX_', 'SG_', 'HR_')

def short(s, n=400):
    s = (s or '').strip()
    return s if len(s) <= n else s[:n] + '…'

def tables(text, rx):
    out = set()
    for m in rx.findall(text):
        n = (m[1] if isinstance(m, tuple) else m).upper()
        if '_' in n and not n.startswith(COL_PREFIX):
            out.add(n)
    return out

def schema_fields(schema, prefix='', depth=0, acc=None):
    acc = [] if acc is None else acc
    if depth > 4 or not isinstance(schema, dict):
        return acc
    for k, v in (schema.get('properties') or {}).items():
        acc.append(prefix + k)
        if isinstance(v, dict):
            schema_fields(v.get('items') if v.get('type') == 'array' else v, prefix + k + '.', depth + 1, acc)
    return acc

def uri_kind(u):
    # mantém só o esquema e o caminho, sem host/porta/parâmetros
    u = re.sub(r'\$\{[^}]*\}', '{cfg}', u.split('?')[0])
    return re.sub(r'^([\w+-]+:(?://)?)[^/]+', r'\1{host}', u) if '://' in u else u

catalogo, tab_idx, api_idx, ev_idx = [], collections.defaultdict(set), collections.defaultdict(set), collections.defaultdict(set)
for f in sorted(glob.glob(os.path.join(SRC, '**', '*.bft'), recursive=True)):
    rel = os.path.relpath(f, SRC)
    try:
        # alguns .bft têm lixo após o JSON: lê só o primeiro objeto
        d = json.JSONDecoder().raw_decode(open(f, encoding='utf-8', errors='ignore').read().lstrip())[0]
    except Exception as e:
        catalogo.append(dict(arquivo=rel, integracao=rel.split(os.sep)[0], erro=str(e)[:120])); continue
    item = dict(arquivo=rel, integracao=rel.split(os.sep)[0])
    item['integracoes'] = [dict(nome=i.get('name'), descricao=short(i.get('description')), documentacao=short(i.get('documentation'), 1500),
                                versao=f"{i.get('majorVersion')}.{i.get('fixVersion')}", liberada=i.get('released'),
                                artefatos=sorted({f"{a.get('type')}: {a.get('name')}" for a in i.get('artifacts', [])}))
                           for i in d.get('integrations', [])]
    evs = []
    for e in d.get('events', []):
        try: sch = json.loads(e.get('schema') or '{}')
        except Exception: sch = {}
        evs.append(dict(nome=e.get('name'), descricao=short(e.get('description')), campos=schema_fields(sch)[:200]))
        ev_idx[e.get('name')].add(rel)
    item['eventos'] = evs
    item['rotas'] = [dict(nome=r.get('name'), evento=r.get('eventName'), fluxo=r.get('mainFlowName'), ativa=r.get('active'),
                          condicao=short(r.get('condition'), 200), versao_min=r.get('tasyInterfacesMinVersion'))
                     for r in d.get('routes', [])]
    item['conectores'] = [dict(nome=c.get('name'), tipo=c.get('type'), descricao=short(c.get('description')),
                               uris=sorted({uri_kind(u) for u in URI.findall(c.get('resource') or '')})[:20])
                          for c in d.get('connectors', [])]
    fl = []
    alltext = ''
    for x in d.get('flows', []):
        res = x.get('resource') or ''
        alltext += res
        fl.append(dict(nome=x.get('name'), descricao=short(x.get('description')),
                       uris=sorted({uri_kind(u) for u in URI.findall(res)})[:20],
                       apis_tasy=sorted(set(APIPATH.findall(res) + [c.get('defaultValue') for c in x.get('configurations', [])
                                         if isinstance(c.get('defaultValue'), str) and '/api/' in c.get('defaultValue')])),
                       metodos_http=sorted({m.upper() for m in METHOD.findall(res)}),
                       tabelas_escrita=sorted(tables(res, SQLW)), tabelas_leitura=sorted(tables(res, SQLR)),
                       procedures=sorted({p.upper() for p in PROC.findall(res)})))
    item['fluxos'] = fl
    item['mapeamentos'] = sorted({m.get('name') for k in ('dataMappings', 'jsonJsonMappings', 'jsonHl7Mappings', 'templateMappings')
                                  for m in d.get(k, []) if m.get('name')})
    for x in fl:
        for t in x['tabelas_escrita'] + x['tabelas_leitura']: tab_idx[t].add(rel)
        for a in x['apis_tasy']: api_idx[re.sub(r'^/tasy-backend/resources', '', a)].add(rel)
    catalogo.append(item)

for r in glob.glob(os.path.join(SRC, '*', '**', 'README.md'), recursive=True) + glob.glob(os.path.join(SRC, '*', '**', '*.MD'), recursive=True):
    dst = os.path.relpath(r, SRC).replace(os.sep, '__')
    shutil.copyfile(r, os.path.join(OUT, 'readmes', dst))

dump = lambda o, n: json.dump(o, open(os.path.join(OUT, n), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
dump(catalogo, 'catalogo.json')
dump({k: sorted(v) for k, v in sorted(api_idx.items())}, 'apis.json')
dump({k: sorted(v) for k, v in sorted(ev_idx.items()) if k}, 'eventos.json')
print(f"bft={len(catalogo)} integracoes={len({c['integracao'] for c in catalogo})} eventos={len(ev_idx)} apis={len(api_idx)}")
