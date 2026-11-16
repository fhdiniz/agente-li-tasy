"""Gerador de documentos, rascunhos, diagramas e classificação. Rodar: uv run pytest"""
import json, os, sys, zipfile

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agente_li import classificar, diagrama, documento, rascunhos
from agente_li.indices import Indices

IDX = Indices()


def _xml(docx):
    return zipfile.ZipFile(docx).read('word/document.xml').decode('utf8')


def test_mascara_segredos_e_poupa_texto_comum():
    assert 'abc12345xyz' not in documento.mascarar('senha: abc12345xyz')
    assert 'eyJhbGciOiJIUzI1NiJ9abc' not in documento.mascarar('Authorization: Bearer eyJhbGciOiJIUzI1NiJ9abc')
    assert documento.mascarar('o token: fixo por ambiente') == 'o token: fixo por ambiente'


@pytest.mark.parametrize('idioma', ['pt-BR', 'es'])
def test_manual_tie_gera_docx_com_secoes_do_modelo(tmp_path, idioma):
    c = rascunhos.manual_tie(IDX, 'mansis/mansis.bft', idioma)
    assert documento.validar(c)['erros'] == []
    r = documento.gerar(c, str(tmp_path / 'm.docx'))
    x = _xml(r['arquivo'])
    assert '4.2.1 Conector' in x and 'surgery.schedule.status.update.cancel' in x
    assert r['amarelos'] > 0 and 'w:highlight' in x
    assert os.path.exists(tmp_path / 'diagramas' / 'fluxo-integracao.drawio')


def test_manual_api_traz_mapeamento_de_tags():
    c = rascunhos.manual_api(IDX, 'Consultation Schedule', 'pt-BR')
    tabelas = [b for s in c['secoes'] for b in s['blocos'] if isinstance(b, dict) and b.get('tipo') == 'tabela']
    assert any('AGENDA_CONSULTA' in json.dumps(t) for t in tabelas)


def test_li_secao_obrigatoria_ausente_e_erro():
    v = documento.validar({'tipo': 'li', 'idioma': 'pt-BR', 'secoes': [{'id': '1', 'titulo': 'Objetivo', 'blocos': ['x']}]})
    assert any('3.2' in e for e in v['erros'])
    with pytest.raises(documento.ErroConteudo):
        documento.gerar({'tipo': 'li', 'idioma': 'pt-BR', 'secoes': []}, '/tmp/nao-gera.docx')


def test_li_rascunho_gera_e_viabilidade_nao_vai_ao_cliente(tmp_path):
    reqs = [{'nome': 'CalendarConsultationScheduleCancellation', 'grupo': 'Agenda', 'metodo': 'PUT', 'operacao': 'escrita', 'resumo': 'Cancela',
             'filtros': '', 'tabela_principal': None, 'tabelas_escrita': {}, 'tabelas_leitura': [], 'colunas': [],
             'procedures': ['ALTERAR_STATUS_AGECONS'], 'funcoes': []}]
    cls = [classificar.classificar(r, IDX) for r in reqs]
    assert cls[0]['classe'] == 'OpenAPI' and 'cancel' in cls[0]['api']
    c = rascunhos.li(reqs, cls, 'es', {'terceiro': 'Terceiro', 'software': 'Portal'})
    assert documento.validar(c)['erros'] == []
    x = _xml(documento.gerar(c, str(tmp_path / 'li.docx'))['arquivo'])
    assert 'CU01' in x and 'Viabilidad' not in x and 'OpenAPI' not in x


def test_cci_preenche_formulario_e_recusa_valor_invalido(tmp_path):
    c = {'tipo': 'cci', 'idioma': 'es', 'campos': {'titulo': 'Cambio X', 'cliente': 'Hospital', 'integracao': 'LIS', 'impactara_em': '4 - Tasy (Producto)'},
         'solicitacao': ['Contexto'], 'solucao': ['Solución', {'tipo': 'tabela', 'colunas': ['A', 'B'], 'linhas': [['1', '2']]}]}
    x = _xml(documento.gerar(c, str(tmp_path / 'cci.docx'))['arquivo'])
    assert 'Cambio X' in x and '[Título del cambio]' not in x and 'Contexto' in x
    c['campos']['impactara_em'] = '9 - Outro'
    assert documento.validar(c)['erros']


def test_diagrama_recusa_loop_e_fim_compartilhado(tmp_path):
    nos = [{'id': 'i', 'tipo': 'inicio', 'raia': 'A'}, {'id': 't', 'tipo': 'tarefa', 'raia': 'A', 'texto': 'x'},
           {'id': 'u', 'tipo': 'tarefa', 'raia': 'A', 'texto': 'y'}, {'id': 'f', 'tipo': 'fim', 'raia': 'A'}]
    ok = {'tipo': 'bpmn', 'titulo': 'T', 'raias': ['A'], 'nos': nos, 'ligacoes': [{'de': 'i', 'para': 't'}, {'de': 't', 'para': 'u'}, {'de': 'u', 'para': 'f'}]}
    assert os.path.exists(diagrama.gerar(ok, str(tmp_path))['drawio'])
    with pytest.raises(diagrama.ErroDiagrama):
        diagrama.gerar(dict(ok, ligacoes=ok['ligacoes'] + [{'de': 'u', 'para': 't'}]), str(tmp_path))
    with pytest.raises(diagrama.ErroDiagrama):
        diagrama.gerar(dict(ok, ligacoes=ok['ligacoes'] + [{'de': 't', 'para': 'f'}]), str(tmp_path))


def test_versao_igual_nos_manifestos():
    import re
    raiz = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    v = {json.load(open(os.path.join(raiz, f), encoding='utf8'))['version'] for f in
         ('.claude-plugin/plugin.json', '.codex-plugin/plugin.json', 'gemini-extension.json')}
    v.add(re.search(r'^version = "([^"]+)"', open(os.path.join(raiz, 'mcp-server', 'pyproject.toml'), encoding='utf8').read(), re.M).group(1))
    assert len(v) == 1, f'versões diferentes nos manifestos: {v}'
    assert f'## {v.pop()} ' in open(os.path.join(raiz, 'CHANGELOG.md'), encoding='utf8').read(), 'versão sem registro no CHANGELOG.md'
