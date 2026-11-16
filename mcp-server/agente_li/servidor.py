"""Servidor MCP local do plugin (stdio). Rodar: uv run --project <plugin>/mcp-server agente-li

Cada ferramenta devolve um recorte pequeno; arquivos grandes (requisitos, classificação, conteúdo) ficam em disco,
na pasta de trabalho indicada pela IA, e as ferramentas trocam só os caminhos.
"""
import json, os

from mcp.server.mcpserver import MCPServer

from . import classificar, diagrama, documento, matriz, rascunhos, terceiro
from .indices import Indices

mcp = MCPServer('agente-li-tasy', instructions=(
    'Base de conhecimento do Tasy (OpenAPI, TIE, PL/SQL) e gerador de LI, Manual e CCI no padrão Bionexo Tasy. '
    'Fluxo: rascunho_* cria um conteudo.json; edite o JSON (seções com "revisar" e [PREENCHER]); validar_documento; gerar_documento. '
    'Nunca escreva senhas ou tokens nos documentos.'))
_idx = None


def idx():
    global _idx
    if _idx is None:
        _idx = Indices()
    return _idx


def _ler(caminho):
    with open(caminho, encoding='utf8') as f:
        return json.load(f)


def _gravar(caminho, dado):
    os.makedirs(os.path.dirname(os.path.abspath(caminho)), exist_ok=True)
    with open(caminho, 'w', encoding='utf8') as f:
        json.dump(dado, f, ensure_ascii=False, indent=1)
    return caminho


@mcp.tool()
def formatos() -> str:
    """Guia dos formatos: conteudo.json (LI, Manual, CCI), blocos, marcação de amarelo, diagramas, requisitos.json e classes de viabilidade.
    Leia uma vez antes de editar um conteudo.json."""
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'formato.md'), encoding='utf8') as f:
        return f.read()


# ------------------------------------------------------------------ documento do terceiro
@mcp.tool()
def ler_documento(caminho: str, inicio: int = 0, tamanho: int = 20000) -> dict:
    """Texto de um PDF (com texto), .docx, .md ou .txt, em fatias. Use quando a ferramenta de IA não lê o arquivo sozinha."""
    ext = os.path.splitext(caminho)[1].lower()
    if ext == '.pdf':
        texto = terceiro.limpar(terceiro.texto_pdf(caminho))
    elif ext == '.docx':
        from docx import Document
        d = Document(caminho)
        texto = '\n'.join(p.text for p in d.paragraphs) + '\n' + '\n'.join(
            ' | '.join(c.text for c in r.cells) for t in d.tables for r in t.rows)
    elif ext in ('.md', '.txt', '.json', '.xml', '.yaml', '.yml', '.csv', '.hl7', '.wsdl'):
        texto = open(caminho, encoding='utf8', errors='replace').read()
    else:
        return {'erro': f'formato não aceito: {ext} (ver docs/decisoes/0011-formatos-de-entrada.md)'}
    return {'total_caracteres': len(texto), 'inicio': inicio, 'texto': texto[inicio:inicio + tamanho]}


@mcp.tool()
def extrair_requisitos(documento_pdf: str, pasta_saida: str, grupo: str = '') -> dict:
    """Extrai os pontos de integração de um PDF no padrão "Resumo / Filtros / SQL" (ex.: Evya 4uHub) para requisitos.json.
    Se o documento tiver outro formato, monte o requisitos.json você mesmo (ver references/requisitos.md) e use analisar_sql."""
    try:
        reqs = [r for r in terceiro.extrair(documento_pdf) if r['grupo'].lower().startswith(grupo.lower())]
    except Exception as e:  # formato diferente: a IA assume a extração
        return {'erro': f'extração automática não se aplica a este documento ({e}). Monte o requisitos.json manualmente.'}
    grupos = {}
    for r in reqs:
        grupos[r['grupo']] = grupos.get(r['grupo'], 0) + 1
    return {'arquivo': _gravar(os.path.join(pasta_saida, 'requisitos.json'), reqs), 'total': len(reqs), 'por_grupo': grupos,
            'escritas': sum(r['operacao'] == 'escrita' for r in reqs)}


@mcp.tool()
def analisar_sql(sql: str) -> dict:
    """Tabelas lidas/gravadas, colunas (TABELA.COLUNA), procedures e funções do Tasy citadas num SQL (schema {database})."""
    return terceiro.analisar_sql(sql)


@mcp.tool()
def classificar_viabilidade(requisitos_json: str, pasta_saida: str, titulo: str = 'Matriz de viabilidade') -> dict:
    """Classifica cada requisito (OpenAPI / Parcial / TIE / Gap) com evidências. Grava classificacao.json e a matriz interna .xlsx
    (não vai ao cliente). Revise você mesmo as linhas de confiança Baixa com buscar_apis/detalhar_api antes de redigir."""
    reqs = _ler(requisitos_json)
    classes = [classificar.classificar(r, idx()) for r in reqs]
    _gravar(os.path.join(pasta_saida, 'classificacao.json'), classes)
    xlsx = os.path.join(pasta_saida, 'matriz-viabilidade-INTERNA.xlsx')
    matriz.gerar([({'numero': n, 'grupo': '', 'titulo': r.get('nome', ''), 'resumo': '', **r}, c) for n, (r, c) in enumerate(zip(reqs, classes), 1)], xlsx, titulo)
    return {'classificacao': os.path.join(pasta_saida, 'classificacao.json'), 'matriz_interna': xlsx,
            'linhas': [{'n': n, 'nome': r['nome'], 'classe': c['classe'], 'confianca': c['confianca'], 'api': c['api'],
                        'cobertura': c['cobertura']} for n, (r, c) in enumerate(zip(reqs, classes), 1)]}


# ------------------------------------------------------------------ base de conhecimento
@mcp.tool()
def buscar_apis(termo: str = '', tabela: str = '', limite: int = 15) -> list:
    """Busca operações das APIs padrão do Tasy (Swagger) por palavras (inglês, como no Swagger) e/ou tabela do Tasy."""
    return idx().buscar_apis(termo, tabela, limite)


@mcp.tool()
def detalhar_api(metodo: str, path: str, limite_campos: int = 80) -> dict:
    """Campos de uma operação: tag JSON, onde aparece, tipo, obrigatório, tabela e coluna do Tasy."""
    o = idx().operacao(metodo, path)
    if not o:
        return {'erro': 'operação não encontrada; use buscar_apis'}
    return {'metodo': o['metodo'], 'path': o['path'], 'api': o['api'], 'swagger': o['arquivo'], 'resumo': o['resumo'],
            'total_campos': len(o['campos']), 'campos': o['campos'][:limite_campos]}


@mcp.tool()
def consultar_tabela(nome: str) -> dict:
    """O que existe no Tasy para uma tabela: APIs OpenAPI, endpoints internos, PL/SQL que grava, eventos e integrações TIE."""
    return idx().tabela(nome) or {'erro': f'tabela {nome} não está nos índices'}


@mcp.tool()
def consultar_plsql(nomes: list[str]) -> dict:
    """Procedures/functions do Tasy pelo nome: assinatura, tabelas que gravam e eventos TIE que disparam."""
    return idx().plsql(nomes)


@mcp.tool()
def buscar_tie(termo: str) -> list:
    """Procura integrações no catálogo TIE (.bft) por nome, evento, fluxo ou API chamada."""
    return idx().buscar_tie(termo)


@mcp.tool()
def detalhar_tie(arquivo: str) -> dict:
    """Conectores, eventos (com gatilhos PL/SQL), fluxos, rotas e mapeamentos de um .bft, mais o README se existir."""
    return idx().tie(arquivo) or {'erro': 'arquivo .bft não encontrado; use buscar_tie'}


# ------------------------------------------------------------------ documentos
@mcp.tool()
def rascunho_manual(pasta_saida: str, idioma: str, arquivo_bft: str = '', api: str = '', nome: str = '') -> dict:
    """Rascunho do Manual de Integração (modelo EMR 12352). Informe arquivo_bft (integração TIE) OU api (título/arquivo do Swagger).
    idioma: pt-BR ou es (pergunte ao consultor). Grava conteudo.json para você completar."""
    if bool(arquivo_bft) == bool(api):
        return {'erro': 'informe arquivo_bft ou api (um dos dois)'}
    c = rascunhos.manual_tie(idx(), arquivo_bft, idioma, nome or None) if arquivo_bft else rascunhos.manual_api(idx(), api, idioma, nome or None)
    return _resumo_rascunho(_gravar(os.path.join(pasta_saida, 'conteudo.json'), c), c)


@mcp.tool()
def rascunho_li(requisitos_json: str, classificacao_json: str, pasta_saida: str, idioma: str, terceiro_nome: str = '', sistema: str = '') -> dict:
    """Rascunho da LI: um caso de uso por requisito, tabela 3.2, de-para da seção 7, GAPs (10) e assuntos abertos (11)."""
    c = rascunhos.li(_ler(requisitos_json), _ler(classificacao_json), idioma, {'terceiro': terceiro_nome, 'software': sistema}, sistema)
    return _resumo_rascunho(_gravar(os.path.join(pasta_saida, 'conteudo.json'), c), c)


def _resumo_rascunho(arquivo, c):
    texto = json.dumps(c, ensure_ascii=False)
    return {'conteudo': arquivo, 'secoes': len(c['secoes']), 'a_completar': texto.count('[PREENCHER') + texto.count('[COMPLETAR') + texto.count('"preencher"'),
            'a_revisar': texto.count('"revisar": true'),
            'proximo_passo': 'reescreva as seções com "revisar" e os [PREENCHER] que souber responder; depois validar_documento e gerar_documento'}


@mcp.tool()
def validar_documento(conteudo_json: str) -> dict:
    """Confere o conteúdo contra a estrutura oficial (seções obrigatórias, valores do CCI)."""
    return documento.validar(_ler(conteudo_json))


@mcp.tool()
def gerar_documento(conteudo_json: str, destino_docx: str) -> dict:
    """Gera o .docx (LI, Manual ou CCI) sobre a base Bionexo Tasy. Ao terminar, repita ao consultor o 'aviso_final'."""
    try:
        return documento.gerar(_ler(conteudo_json), destino_docx)
    except (documento.ErroConteudo, diagrama.ErroDiagrama) as e:
        return {'erro': str(e)}


@mcp.tool()
def gerar_diagrama(modelo: dict, pasta_saida: str) -> dict:
    """Valida e desenha um diagrama (bpmn | casos_de_uso | sequencia). Entrega .drawio (editável), .png e .json."""
    try:
        return diagrama.gerar(modelo, pasta_saida)
    except diagrama.ErroDiagrama as e:
        return {'erro': str(e)}


def main():
    mcp.run()


if __name__ == '__main__':
    main()
