"""Gera a matriz de viabilidade interna (.xlsx). Uso interno: não vai ao cliente."""
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

AMARELO = PatternFill('solid', fgColor='FFFF00')
CAB = PatternFill('solid', fgColor='1F4E79')
CORES = {'OpenAPI': 'C6EFCE', 'Parcial': 'DDEBF7', 'TIE': 'FCE4D6', 'Gap': 'F8CBAD'}
COLS = [('ID', 6), ('Grupo', 16), ('Endpoint do terceiro', 34), ('Método', 8), ('Operação', 9), ('Resumo', 50),
        ('Tabela principal', 22), ('Viabilidade', 11), ('Confiança', 10), ('API Tasy sugerida', 48), ('Swagger', 24),
        ('Cobertura de colunas', 11), ('Colunas sem cobertura na API', 45), ('Alternativas', 48), ('Eventos TIE', 30),
        ('Integrações TIE na tabela', 30), ('Procedures chamadas', 30), ('Justificativa', 60),
        ('Viabilidade correta? (consultor)', 14), ('Classe correta (consultor)', 14), ('Comentário do consultor', 40)]


def gerar(linhas, destino, titulo):
    wb = Workbook(); ws = wb.active; ws.title = 'Matriz'
    ws['A1'] = f'{titulo} — USO INTERNO, NÃO ENVIAR AO CLIENTE'; ws['A1'].font = Font(bold=True, size=13, color='C00000')
    ws['A2'] = 'O que está em amarelo cabe análise do consultor.'; ws['A2'].fill = AMARELO
    for i, (nome, larg) in enumerate(COLS, 1):
        c = ws.cell(4, i, nome); c.fill = CAB; c.font = Font(bold=True, color='FFFFFF')
        c.alignment = Alignment(wrap_text=True, vertical='center')
        ws.column_dimensions[c.column_letter].width = larg
    dv1 = DataValidation(type='list', formula1='"Sim,Não"', allow_blank=True)
    dv2 = DataValidation(type='list', formula1='"OpenAPI,Parcial,TIE,Gap"', allow_blank=True)
    ws.add_data_validation(dv1); ws.add_data_validation(dv2)
    for r, (req, c) in enumerate(linhas, 5):
        vals = [req['numero'], req['grupo'], req['titulo'], req['metodo'], req['operacao'], req['resumo'],
                c['tabela_principal'] or '', c['classe'], c['confianca'], c['api'], c['swagger'],
                c['cobertura'] if c['api'] else '', ', '.join(c['colunas_sem_cobertura'][:25]) +
                (f" (+{len(c['colunas_sem_cobertura']) - 25})" if len(c['colunas_sem_cobertura']) > 25 else ''),
                '\n'.join(c['alternativas']), ', '.join(c['tie_eventos'][:8]), ', '.join(c['tie_integracoes'][:10]),
                ', '.join(req.get('procedures', [])), c['justificativa'], '', '', '']
        for i, v in enumerate(vals, 1):
            cell = ws.cell(r, i, v); cell.alignment = Alignment(wrap_text=True, vertical='top')
        ws.cell(r, 8).fill = PatternFill('solid', fgColor=CORES[c['classe']])
        ws.cell(r, 12).number_format = '0%'
        if c['confianca'] == 'Baixa':
            for i in (8, 9, 10):
                ws.cell(r, i).fill = AMARELO
        dv1.add(ws.cell(r, 19)); dv2.add(ws.cell(r, 20))
    ws.freeze_panes = 'D5'; ws.auto_filter.ref = f'A4:{ws.cell(4, len(COLS)).column_letter}{4 + len(linhas)}'

    lg = wb.create_sheet('Legenda')
    for row in [
        ('Viabilidade', 'Significado'),
        ('OpenAPI', 'Existe API padrão (Swagger) que cobre o requisito e a maior parte dos campos.'),
        ('Parcial', 'Existe API padrão do mesmo assunto, mas não expõe todos os campos/filtros que o terceiro usa (ver "Colunas sem cobertura").'),
        ('TIE', 'Sem API padrão. Viável fora do Open via TIE: leitura por consulta, procedure do Tasy ou evento TIE já existente.'),
        ('Gap', 'Escrita direta em tabela sem API nem procedure do Tasy: exige desenvolvimento/produto.'),
        ('', ''),
        ('Confiança', 'Alta: API do mesmo tipo, nota >= 0,70 e cobertura >= 60%. Baixa (amarelo): API de outro tipo de agenda, cobertura < 25% ou sem evidência forte.'),
        ('Cobertura', '70% colunas da tabela principal + 30% das demais tabelas usadas no SQL do terceiro.'),
        ('Fonte', 'Swaggers em referencias/openapi; índices do TIE e PL/SQL em referencias/indices. Classificação determinística (mcp-server/agente_li/classificar.py).'),
    ]:
        lg.append(row)
    lg['A1'].font = lg['B1'].font = Font(bold=True)
    lg.column_dimensions['A'].width = 14; lg.column_dimensions['B'].width = 120
    wb.save(destino)
