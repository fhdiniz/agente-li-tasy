"""Classificação determinística de viabilidade: OpenAPI / Parcial / TIE / Gap.

Regras (iguais para qualquer terceiro; a IA só revisa o que vier com confiança Baixa):
1. Candidatas = operações OpenAPI que expõem a tabela principal do requisito.
2. Nota = fator_método x (0,35 tabela + 0,30 cobertura de colunas + 0,35 palavras-chave).
3. Nota >= NOTA_OK e cobertura >= COB_OK -> OpenAPI; nota >= NOTA_PARCIAL -> Parcial.
4. Sem API: TIE se for leitura (o TIE consulta o banco), se a escrita for feita por procedure do Tasy
   ou se houver evento/integração TIE na tabela; senão Gap (escrita direta sem regra de negócio do Tasy).
"""
import re

NOTA_OK, NOTA_PARCIAL, COB_OK = 0.55, 0.40, 0.60
# palavra do terceiro -> radicais que aparecem em paths/resumos do Tasy
SINONIMOS = {
    'calendar': ['schedul'], 'schedule': ['schedul'], 'scheduling': ['schedul', 'book', 'record'],
    'consultation': ['consult'], 'consul': ['consult'], 'exam': ['exam'], 'appointment': ['appointment', 'schedul'],
    'available': ['available', 'slot', 'time'], 'availability': ['available', 'slot', 'time'],
    'cancellation': ['cancel', 'status'], 'confirmation': ['confirm', 'status'], 'checkin': ['status', 'check'],
    'reason': ['reason'], 'procedure': ['procedure'], 'specialty': ['specialt'], 'grouping': ['group'],
    'preference': ['preference'], 'price': ['price'], 'register': ['schedules'], 'individual': ['natural', 'person'],
    'insurance': ['insurance'], 'encounter': ['encounter'], 'patient': ['patient'],
    # português / espanhol
    'agenda': ['schedul'], 'agendamento': ['schedul', 'appointment'], 'cita': ['appointment', 'schedul'],
    'consulta': ['consult'], 'exame': ['exam'], 'examen': ['exam'], 'horario': ['slot', 'available', 'time'],
    'disponivel': ['available', 'slot'], 'disponible': ['available', 'slot'], 'cancelamento': ['cancel', 'status'],
    'cancelacion': ['cancel', 'status'], 'confirmacao': ['confirm', 'status'], 'confirmacion': ['confirm', 'status'],
    'motivo': ['reason'], 'procedimento': ['procedure'], 'procedimiento': ['procedure'], 'especialidade': ['specialt'],
    'especialidad': ['specialt'], 'pessoa': ['person', 'natural'], 'persona': ['person', 'natural'],
    'paciente': ['patient'], 'atendimento': ['encounter'], 'atencion': ['encounter'], 'convenio': ['insurance'],
    'medico': ['practitioner', 'physician'], 'fatura': ['invoice'], 'factura': ['invoice'], 'titulo': ['receivable', 'payable'],
    'estoque': ['stock'], 'material': ['material'], 'prescricao': ['prescription'], 'laudo': ['report', 'result'],
    'resultado': ['result'], 'laboratorio': ['laborator'], 'beneficiario': ['insured'], 'setor': ['department', 'sector'],
}
# especializações de agenda: se o path da API tem uma e o requisito não, a API é de outro tipo de agenda
QUALIFICADORES = {'surgical', 'consultation', 'exam', 'integrated'}
IGNORAR = {'all', 'by', 'date', 'code', 'web', 'bot', 'controller', 'for', 'and', 'inquiry', 'billing', 'data', 'list'}


def _tokens_terceiro(nome):
    from .indices import norm
    partes = re.findall(r'[A-Z]?[a-zà-ú]+|[A-Z]+(?![a-z])', nome)
    return [w for w in (norm(p) for p in partes) if w and w not in IGNORAR and len(w) > 1]


def _palavras_path(path):
    return {w.lower() for w in re.findall(r'[A-Z]?[a-z]+', path)}


def _kw(palavras, op):
    """Peso 1 se o radical está no path, 0,5 se só no resumo; o 1º sinônimo vale mais que os demais."""
    total = 0.0
    for p in palavras:
        melhor = 0.0
        for i, r in enumerate(SINONIMOS.get(p, [p])):
            peso = 1.0 if i == 0 else 0.7
            if any(w.startswith(r) for w in op['_path']):
                melhor = max(melhor, peso)
            elif re.search(r'\b' + r, op['_resumo']):
                melhor = max(melhor, 0.5 * peso)
        total += melhor
    nota = total / max(len(palavras), 1)
    estranhos = {q for q in QUALIFICADORES if q in op['_path']} - {SINONIMOS.get(p, [p])[0].rstrip('ul') for p in palavras} - set(palavras)
    estranhos = {q for q in estranhos if not any(q.startswith(SINONIMOS.get(p, [p])[0]) for p in palavras)}
    return nota * (0.5 if estranhos else 1.0), bool(estranhos)


def _metodo(req, op):
    if req['operacao'] == 'leitura':
        return 1.0 if op['metodo'] == 'GET' else 0.2
    if op['metodo'] == 'GET':
        return 0.1
    if req['metodo'] == 'POST' and op['metodo'] == 'POST':
        return 1.0
    return 1.0 if op['metodo'] in ('PUT', 'PATCH', 'POST') else 0.5


def _cobertura(reqcols, principal, op):
    """70% colunas da tabela principal + 30% demais (joins de descrição pesam menos)."""
    if not reqcols:
        return 1.0 if principal in op['_tabs'] else 0.0
    prin = {c for c in reqcols if c.startswith(principal + '.')}
    outras = reqcols - prin
    cp = len(prin & op['_cols']) / len(prin) if prin else None
    co = len(outras & op['_cols']) / len(outras) if outras else None
    if cp is None or co is None:
        return cp if co is None else co
    return 0.7 * cp + 0.3 * co


def classificar(req, idx):
    principal = req['tabela_principal']
    procs = idx.plsql(req.get('procedures') or [])
    procs = {n: p for n, p in procs.items() if p and p['tipo'] in ('procedure', 'function')}
    grava_proc = sorted({t for p in procs.values() if p for t in p['grava']})
    if not principal and procs:  # escrita só por procedure: a tabela vem do PL/SQL
        alvo = [t for t in grava_proc if t.startswith('AGENDA')] or grava_proc
        principal = alvo[0] if alvo else None
    reqcols = set(req['colunas'])
    reqtabs = {c.split('.')[0] for c in reqcols} | ({principal} if principal else set())
    palavras = _tokens_terceiro(req['nome'])
    req = {'tabelas_escrita': {}, 'procedures': [], 'funcoes': [], **req}

    cands = []
    for op in idx.ops:
        if principal not in op['_tabs'] and not (reqtabs & op['_tabs']):
            continue
        tab = 1.0 if principal in op['_tabs'] else 0.4 * len(reqtabs & op['_tabs']) / max(len(reqtabs), 1)
        cob = _cobertura(reqcols, principal, op)
        kw, outro_tipo = _kw(palavras, op)
        nota = _metodo(req, op) * (0.35 * tab + 0.30 * cob + 0.35 * kw)
        cands.append({'nota': round(nota, 3), 'cobertura': round(cob, 2), 'op': op, 'outro_tipo': outro_tipo})
    cands.sort(key=lambda c: -c['nota'])
    melhor = cands[0] if cands else None
    segunda = cands[1]['nota'] if len(cands) > 1 else 0

    t = idx.tabelas.get(principal or '', {})
    # de-para sugerido: coluna usada pelo terceiro -> tag JSON da API escolhida (alimenta a seção 7 da LI)
    depara = []
    if melhor:
        por_col = {}
        for c in melhor['op']['campos']:
            if c['tabela']:
                por_col.setdefault(f"{c['tabela']}.{c['coluna']}", c)
        depara = [{'coluna': col, 'campo_api': por_col[col]['nome'], 'em': por_col[col]['em'], 'tipo': por_col[col]['tipo']}
                  for col in sorted(reqcols) if col in por_col]
    tie_ev = t.get('tie_eventos', {}).get('itens', [])
    tie_int = t.get('tie_integracoes', {}).get('itens', [])
    tie_proc = sorted({e for p in procs.values() if p for e in p['eventos_tie']})

    if melhor and melhor['nota'] >= NOTA_OK and melhor['cobertura'] >= COB_OK:
        classe = 'OpenAPI'
    elif melhor and melhor['nota'] >= NOTA_PARCIAL:
        classe = 'Parcial'
    elif tie_ev or tie_int or tie_proc or req['operacao'] == 'leitura' or (procs and any(procs.values())):
        classe = 'TIE'
    else:
        classe = 'Gap'

    if classe in ('OpenAPI', 'Parcial'):
        margem = melhor['nota'] - segunda
        if melhor['outro_tipo'] or melhor['cobertura'] < 0.25 or melhor['nota'] < 0.50:
            conf = 'Baixa'  # API de outro tipo de agenda, ou cobre pouco do que o terceiro usa
        elif melhor['nota'] >= 0.70 and melhor['cobertura'] >= 0.60 and (margem >= 0.05 or melhor['cobertura'] >= 0.8):
            conf = 'Alta'
        else:
            conf = 'Média'
    elif classe == 'TIE':
        conf = 'Média' if (tie_ev or tie_proc or (procs and any(procs.values()))) else 'Baixa'
    else:  # Gap é afirmação forte: se o terceiro chama função/procedure do Tasy, o TIE talvez resolva
        conf = 'Baixa' if cands or req.get('funcoes') or req.get('procedures') else 'Média'

    faltam = sorted(reqcols - melhor['op']['_cols']) if melhor else sorted(reqcols)
    just = []
    if melhor:
        o = melhor['op']
        just.append(f"Melhor API: {o['metodo']} {o['path']} (nota {melhor['nota']}, cobre {int(melhor['cobertura']*100)}% das colunas)")
    else:
        just.append('Nenhuma operação OpenAPI expõe as tabelas do requisito')
    if req['operacao'] == 'escrita' and not req['tabelas_escrita'] and procs:
        just.append('Escrita via procedure ' + ', '.join(req['procedures']))
    if classe == 'TIE':
        if tie_ev or tie_proc:
            just.append('Evento TIE já disparado na tabela/procedure: ' + ', '.join((tie_ev + tie_proc)[:4]))
        elif req['operacao'] == 'leitura':
            just.append('Sem API padrão: leitura viável por consulta SQL em integração TIE')
        else:
            just.append('Sem API padrão: TIE pode chamar a procedure do Tasy')
    if classe == 'Gap':
        just.append('Escrita direta em tabela sem procedure/API do Tasy: exige desenvolvimento')
    return {
        'classe': classe, 'confianca': conf, 'tabela_principal': principal,
        'api': f"{melhor['op']['metodo']} {melhor['op']['path']}" if melhor else '',
        'swagger': melhor['op']['arquivo'] if melhor else '', 'nota': melhor['nota'] if melhor else 0,
        'cobertura': melhor['cobertura'] if melhor else 0, 'colunas_sem_cobertura': faltam,
        'alternativas': [f"{c['op']['metodo']} {c['op']['path']} ({c['nota']})" for c in cands[1:4]],
        'tie_eventos': tie_ev + [e for e in tie_proc if e not in tie_ev], 'tie_integracoes': tie_int,
        'procedures_grava': grava_proc, 'justificativa': '; '.join(just), 'depara': depara,
    }
