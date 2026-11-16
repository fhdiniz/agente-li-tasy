"""Consultas à base de conhecimento do Tasy (referencias/indices + Swaggers).

Tudo aqui devolve recortes pequenos: a IA nunca recebe um índice inteiro.
"""
import json, os, re, unicodedata
from functools import cached_property

from . import openapi_idx


def raiz_padrao():
    return os.environ.get('AGENTE_LI_RAIZ') or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def norm(texto):
    t = unicodedata.normalize('NFKD', str(texto)).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', ' ', t).strip()


class Indices:
    def __init__(self, raiz=None):
        self.raiz = raiz or raiz_padrao()
        self.pasta = os.path.join(self.raiz, 'referencias', 'indices')
        self._plsql = {}

    def _json(self, *partes):
        with open(os.path.join(self.pasta, *partes), encoding='utf8') as f:
            return json.load(f)

    # ---------- OpenAPI ----------
    @cached_property
    def ops(self):
        """Operações únicas por método+path (a mesma operação aparece em mais de um Swagger)."""
        unicas = {}
        for op in openapi_idx.carregar(self.raiz):
            k = (op['metodo'], op['path'])
            if k in unicas:
                u = unicas[k]
                u['arquivo'] += ', ' + op['arquivo']
                u['colunas'] = sorted(set(u['colunas']) | set(op['colunas']))
                nomes = {(c['nome'], c['em']) for c in u['campos']}
                u['campos'] += [c for c in op['campos'] if (c['nome'], c['em']) not in nomes]
            else:
                unicas[k] = dict(op, campos=list(op['campos']))
        ops = list(unicas.values())
        for op in ops:
            op['_tabs'] = {c.split('.')[0] for c in op['colunas']}
            op['_cols'] = set(op['colunas'])
            op['_path'] = {w.lower() for w in re.findall(r'[A-Z]?[a-z]+', op['path'])}
            op['_resumo'] = op['resumo'].lower()
        return ops

    def operacao(self, metodo, path):
        return next((o for o in self.ops if o['metodo'] == metodo.upper() and o['path'] == path), None)

    def buscar_apis(self, termo='', tabela='', limite=15):
        """Busca operações por palavras (path, resumo, API) e/ou por tabela do Tasy."""
        palavras = norm(termo).split()
        tabela = tabela.upper().strip()
        achados = []
        for o in self.ops:
            if tabela and tabela not in o['_tabs']:
                continue
            texto = norm(f"{o['path']} {o['resumo']} {o['api']} {' '.join(o['tags'])}")
            pontos = sum(p in texto for p in palavras)
            if palavras and not pontos:
                continue
            achados.append((pontos, o))
        achados.sort(key=lambda a: (-a[0], a[1]['path']))
        return [resumo_op(o) for _, o in achados[:limite]]

    # ---------- Tabelas ----------
    @cached_property
    def tabelas(self):
        return self._json('tabelas.json')

    def tabela(self, nome, itens=12):
        t = self.tabelas.get(nome.upper().strip())
        if t is None:
            return None
        r = {k: {'total': v['total'], 'itens': v['itens'][:itens]} for k, v in t.items()}
        cols = sorted({c for e in self.entidades.get(nome.upper().strip(), []) for c in e['colunas']})
        if cols:
            r['colunas_conhecidas'] = cols[:120]
        return r

    @cached_property
    def entidades(self):
        return self._json('interfaces', 'entidades.json')

    # ---------- PL/SQL ----------
    def plsql(self, nomes):
        """Objetos PL/SQL pelo nome (procedure, function, package, trigger): tabelas gravadas/lidas e eventos TIE."""
        nomes = [n.upper() for n in nomes]
        falta = {n for n in nomes if n not in self._plsql}
        if falta:
            with open(os.path.join(self.pasta, 'plsql', 'objetos.jsonl'), encoding='utf8') as f:
                for linha in f:
                    if any(f'"{n}"' in linha for n in falta):
                        o = json.loads(linha)
                        if o.get('n') in falta and o['n'] not in self._plsql:
                            self._plsql[o['n']] = {'tipo': o['t'], 'schema': o.get('s', ''), 'assinatura': o.get('sig', '')[:400],
                                                   'descricao': o.get('desc', '')[:300], 'grava': o.get('w', []),
                                                   'le': o.get('r', [])[:40], 'tabela_trigger': o.get('on'),
                                                   'eventos_tie': o.get('ev', [])}
            for n in falta:
                self._plsql.setdefault(n, None)
        return {n: self._plsql[n] for n in nomes}

    @cached_property
    def _triggers(self):
        """Triggers por conjunto de palavras do nome, para achar o gatilho de eventos que o extrator não ligou."""
        mapa = {}
        with open(os.path.join(self.pasta, 'plsql', 'objetos.jsonl'), encoding='utf8') as f:
            for linha in f:
                if '"t": "trigger"' in linha or '"t":"trigger"' in linha:
                    o = json.loads(linha)
                    chave = frozenset(norm(o['n']).split()) - {'tie', 'api', 'hl7'}
                    mapa.setdefault(chave, {'objeto': f"{o.get('s', '')}.{o['n']} (trigger)", 'tabela_trigger': o.get('on'), 'payload': None})
        return mapa

    @cached_property
    def eventos_plsql(self):
        return self._json('plsql', 'eventos_tie.json')

    # ---------- TIE ----------
    @cached_property
    def catalogo(self):
        return [b for b in self._json('tie', 'catalogo.json') if 'erro' not in b]

    def buscar_tie(self, termo, limite=20):
        """Lista arquivos .bft cujo nome, integração, evento, fluxo ou API combine com o termo."""
        palavras = norm(termo).split()
        achados = []
        for b in self.catalogo:
            nomes = [b['arquivo']] + [i['nome'] + ' ' + i.get('descricao', '') for i in b['integracoes']] + \
                    [e['nome'] for e in b['eventos']] + [f['nome'] for f in b['fluxos']] + \
                    [a for f in b['fluxos'] for a in f['apis_tasy']] + [c['nome'] for c in b['conectores']]
            texto = norm(' '.join(nomes))
            pontos = sum(p in texto for p in palavras)
            if pontos == len(palavras) and palavras:
                achados.append({'arquivo': b['arquivo'], 'integracao': b['integracao'],
                                'nomes': [i['nome'] for i in b['integracoes']],
                                'eventos': len(b['eventos']), 'rotas': len(b['rotas']), 'fluxos': len(b['fluxos']),
                                'conectores': len(b['conectores']), 'mapeamentos': len(b['mapeamentos'])})
        return achados[:limite]

    def tie(self, arquivo):
        """Detalhe de um .bft, com os gatilhos PL/SQL de cada evento e o README, se houver."""
        b = next((b for b in self.catalogo if b['arquivo'] == arquivo), None) or \
            next((b for b in self.catalogo if norm(arquivo) in norm(b['arquivo'])), None)
        if not b:
            return None
        b = json.loads(json.dumps(b))
        for e in b['eventos']:
            e['gatilhos'] = self.eventos_plsql.get(e['nome']) or []
            if not e['gatilhos']:  # inferência pelo nome: o rascunho marca como "a confirmar"
                achado = self._triggers.get(frozenset(norm(e['nome']).split()) - {'tie', 'api', 'hl7'})
                if achado:
                    e['gatilhos'] = [dict(achado, inferido=True)]
        leiame = os.path.join(self.pasta, 'tie', 'readmes', '__'.join(b['arquivo'].split('/')[:-1]) + '__README.md')
        b['readme'] = open(leiame, encoding='utf8').read()[:6000] if os.path.exists(leiame) else ''
        return b


def resumo_op(o):
    return {'metodo': o['metodo'], 'path': o['path'], 'api': o['api'], 'swagger': o['arquivo'], 'resumo': o['resumo'][:160],
            'tabelas': sorted(o['_tabs'])[:8], 'campos': len(o['campos'])}
