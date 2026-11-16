"""Autoteste do parser de SQL do terceiro. Rodar: python3 -m pytest testes  (ou python3 testes/test_terceiro_sql.py)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agente_li.terceiro import analisar_sql


def test_update_com_alias_e_funcao():
    r = analisar_sql("UPDATE {database}.agenda_consulta SET nr_atendimento = :x , ie_status_agenda = 'AR' WHERE nr_sequencia = :id")
    assert r['tabelas_escrita'] == {'AGENDA_CONSULTA': 'UPDATE'}
    assert {'AGENDA_CONSULTA.NR_ATENDIMENTO', 'AGENDA_CONSULTA.IE_STATUS_AGENDA'} <= set(r['colunas'])


def test_select_alias_e_funcao_nao_vira_tabela():
    r = analisar_sql("SELECT a.cd_agenda, {database}.obter_nome_pf(a.cd_pessoa_fisica) FROM {database}.agenda a WHERE a.ie_situacao = 'A'")
    assert r['tabelas_leitura'] == ['AGENDA'] and r['funcoes'] == ['OBTER_NOME_PF']
    assert r['tabela_principal'] == 'AGENDA' and 'AGENDA.CD_PESSOA_FISICA' in r['colunas']


def test_procedure_em_bloco_begin():
    r = analisar_sql("begin {database}.alterar_status_agecons(:a, :b, 'C'); end;")
    assert r['procedures'] == ['ALTERAR_STATUS_AGECONS'] and r['tabelas_leitura'] == []


if __name__ == '__main__':
    for n, f in list(globals().items()):
        if n.startswith('test_'):
            f(); print('ok', n)
