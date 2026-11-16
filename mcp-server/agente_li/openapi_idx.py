"""Índice de operações dos Swaggers/OpenAPI do Tasy.

Para cada operação guarda os campos (tag JSON, onde aparece, tipo, obrigatório) e a tabela/coluna do Tasy
que o Swagger declara em "**Referenced Table:** X / **Referenced Column:** Y".
Gera referencias/indices/openapi/operacoes.json (versionável; recriado sozinho se os Swaggers mudarem).
"""
import glob, json, os, re

REF = re.compile(r'Referenced Table:\**\s*([A-Za-z0-9_$]+)\s*(?:\\n|\s)*\**Referenced Column:\**\s*([A-Za-z0-9_$]+)')
METODOS = {'get', 'post', 'put', 'patch', 'delete'}
VERSAO = 2  # mudar quando o formato do índice mudar


def _resolver(doc, ref):
    no = doc
    for parte in ref.lstrip('#/').split('/'):
        no = no.get(parte, {}) if isinstance(no, dict) else {}
    return no


def _limpar(desc):
    desc = re.sub(r'\**Referenced (Table|Column):\**\s*[A-Za-z0-9_$]+', '', desc or '')
    return ' '.join(desc.split())[:200]


def _campo(nome, onde, no, obrig):
    desc = no.get('description') or ''
    m = REF.search(desc)
    tipo = no.get('type') or ('object' if 'properties' in no else '')
    if no.get('format'):
        tipo += f" ({no['format']})"
    return {'nome': nome, 'em': onde, 'tipo': tipo, 'obrigatorio': bool(obrig), 'descricao': _limpar(desc),
            'tabela': m.group(1).upper() if m else '', 'coluna': m.group(2).upper() if m else ''}


def _schema(doc, no, onde, prefixo, vistos, out, nivel=0):
    """Achata um schema (com $ref) em campos 'a.b[].c'."""
    if not isinstance(no, dict) or nivel > 6:
        return
    if '$ref' in no:
        if no['$ref'] in vistos:
            return
        vistos = vistos | {no['$ref']}
        no = _resolver(doc, no['$ref'])
    for sub in no.get('allOf', []):
        _schema(doc, sub, onde, prefixo, vistos, out, nivel)
    if no.get('type') == 'array' or 'items' in no:
        _schema(doc, no.get('items', {}), onde, prefixo + '[]', vistos, out, nivel + 1)
        return
    obrig = set(no.get('required', []))
    for nome, prop in (no.get('properties') or {}).items():
        if not isinstance(prop, dict):
            continue
        alvo = _resolver(doc, prop['$ref']) if '$ref' in prop else prop
        caminho = f'{prefixo}.{nome}' if prefixo else nome
        if alvo.get('type') == 'array' or 'properties' in alvo or 'items' in alvo or 'allOf' in alvo:
            _schema(doc, prop, onde, caminho, vistos, out, nivel + 1)
        else:
            out.append(_campo(caminho, onde, {**alvo, 'description': prop.get('description') or alvo.get('description')},
                              nome in obrig))


def _operacao(doc, item, op):
    campos = []
    for p in list(item.get('parameters', [])) + list(op.get('parameters', [])):
        if '$ref' in p:
            p = _resolver(doc, p['$ref'])
        if p.get('in') == 'body':  # Swagger 2
            _schema(doc, p.get('schema', {}), 'corpo', '', frozenset(), campos)
        else:
            campos.append(_campo(p.get('name', ''), p.get('in', ''), {**p.get('schema', {}), **p}, p.get('required')))
    for conteudo in (op.get('requestBody', {}).get('content') or {}).values():  # OpenAPI 3
        _schema(doc, conteudo.get('schema', {}), 'corpo', '', frozenset(), campos)
        break
    for cod, resp in (op.get('responses') or {}).items():
        if not str(cod).startswith('2') or not isinstance(resp, dict):
            continue
        esquemas = [resp['schema']] if 'schema' in resp else [c.get('schema', {}) for c in (resp.get('content') or {}).values()][:1]
        for s in esquemas:
            _schema(doc, s, 'resposta', '', frozenset(), campos)
    vistos, unicos = set(), []
    for c in campos:
        k = (c['nome'], c['em'])
        if k not in vistos:
            vistos.add(k); unicos.append(c)
    return unicos


def construir(pasta_openapi):
    ops = []
    for f in sorted(glob.glob(os.path.join(pasta_openapi, '*.json'))):
        doc = json.load(open(f, encoding='utf8'))
        for path, item in doc.get('paths', {}).items():
            for m, op in item.items():
                if m not in METODOS or not isinstance(op, dict):
                    continue
                campos = _operacao(doc, item, op)
                resumo = (op.get('summary') or op.get('description') or '').strip().split('\n')[0][:300]
                ops.append({'arquivo': os.path.basename(f), 'api': (doc.get('info') or {}).get('title', ''),
                            'metodo': m.upper(), 'path': path, 'resumo': resumo,
                            'tags': op.get('tags', []), 'campos': campos,
                            'colunas': sorted({f"{c['tabela']}.{c['coluna']}" for c in campos if c['tabela']})})
    return ops


def carregar(raiz_repo):
    destino = os.path.join(raiz_repo, 'referencias', 'indices', 'openapi', 'operacoes.json')
    fontes = glob.glob(os.path.join(raiz_repo, 'referencias', 'openapi', '*.json'))
    atual = None
    if os.path.exists(destino) and (not fontes or max(map(os.path.getmtime, fontes)) <= os.path.getmtime(destino)):
        atual = json.load(open(destino, encoding='utf8'))
        if not isinstance(atual, dict) or atual.get('versao') != VERSAO:
            atual = None
    if atual is None:
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        atual = {'versao': VERSAO, 'operacoes': construir(os.path.join(raiz_repo, 'referencias', 'openapi'))}
        json.dump(atual, open(destino, 'w', encoding='utf8'), ensure_ascii=False, separators=(',', ':'))
    return atual['operacoes']
