"""Cruza os índices gerados (OpenAPI, tasy-interfaces, PL/SQL, TIE) num índice único por tabela.

Uso: python montar_indice_tabelas.py <pasta referencias>
Lê referencias/openapi/*.json e referencias/indices/{interfaces,plsql,tie}; grava referencias/indices/tabelas.json.
Não depende dos .zip: pode ser reexecutado a qualquer momento.
"""
import json, os, re, sys, glob, collections

REF = sys.argv[1]
IDX = os.path.join(REF, 'indices')
load = lambda *p: json.load(open(os.path.join(IDX, *p), encoding='utf-8'))
T = collections.defaultdict(lambda: collections.defaultdict(set))

# 1. OpenAPI: "**Referenced Table:**" nas descrições
RT = re.compile(r'\*\*Referenced Table:\*\*\s*([A-Z0-9_]+)')
for f in glob.glob(os.path.join(REF, 'openapi', '*.json')):
    d = json.load(open(f, encoding='utf-8'))
    for path, item in (d.get('paths') or {}).items():
        for m, o in item.items():
            if m.lower() not in ('get', 'post', 'put', 'patch', 'delete'):
                continue
            txt = json.dumps(o)
            for sref in re.findall(r'#/components/schemas/([\w.-]+)', txt):
                txt += json.dumps((d.get('components', {}).get('schemas', {}) or {}).get(sref, {}))
            for t in set(RT.findall(txt)):
                T[t]['openapi'].add(f"{m.upper()} {path} [{os.path.basename(f)}]")

# 2. tasy-interfaces: endpoints e entidades
for e in load('interfaces', 'endpoints.json'):
    ref = f"{e['metodo']} {e['path']} [{e['modulo']}]"
    for t in e['tabelas_escrita_sql']: T[t]['interfaces_escrita'].add(ref)
    for t in e['entidades_jpa']: T[t]['interfaces_jpa'].add(ref)
for t, ents in load('interfaces', 'entidades.json').items():
    T[t]['entidades_jpa'] |= {f"{x['modulo']}.{x['classe']}" for x in ents}

# 3. PL/SQL: quem grava; triggers que disparam eventos TIE
for t, objs in load('plsql', 'tabelas_escrita.json').items():
    T[t]['plsql_escrita'] |= set(objs)
ev_bft = load('tie', 'eventos.json')
for ev, lst in load('plsql', 'eventos_tie.json').items():
    for x in lst:
        if x['tabela_trigger']:
            T[x['tabela_trigger']]['tie_eventos'].add(ev)
            T[x['tabela_trigger']]['tie_integracoes'] |= {b.split('/')[0] for b in ev_bft.get(ev, [])}

# 4. TIE: APIs do Tasy chamadas pelos fluxos -> tabelas dessas APIs (via interfaces)
api_tie = load('tie', 'apis.json')
def norm(p): return re.sub(r'\{[^}]*\}|\$\{[^}]*\}?.*', '{}', p).rstrip('/')
api_tabs = collections.defaultdict(set)
for e in load('interfaces', 'endpoints.json'):
    api_tabs[norm(e['path'])] |= set(e['tabelas_escrita_sql']) | set(e['entidades_jpa'])
for api, bfts in api_tie.items():
    for t in api_tabs.get(norm(api), ()):
        T[t]['tie_integracoes'] |= {b.split('/')[0] for b in bfts}

LIMIT = 40  # evita índice gigante: guarda total e uma amostra
out = {}
for t in sorted(T):
    out[t] = {k: {'total': len(v), 'itens': sorted(v)[:LIMIT]} for k, v in sorted(T[t].items())}
json.dump(out, open(os.path.join(IDX, 'tabelas.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f"tabelas={len(out)} com_api={sum(1 for v in out.values() if 'openapi' in v or 'interfaces_escrita' in v or 'interfaces_jpa' in v)}")
