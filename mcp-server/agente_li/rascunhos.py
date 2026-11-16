"""Rascunhos determinísticos de conteúdo (JSON) para o gerador de documentos.

O código preenche o que está nos índices (conector, evento, fluxo, rota, APIs, de-para). O que depende de
interpretação sai marcado com "revisar": true ou [PREENCHER: ...] — a IA reescreve esses trechos e o consultor valida.
"""
import re

ESQUEMAS = {  # esquema da URI Camel -> (forma de comunicação pt, es)
    'http4': ('HTTP/REST', 'HTTP/REST'), 'https4': ('HTTPS/REST', 'HTTPS/REST'), 'http': ('HTTP/REST', 'HTTP/REST'),
    'https': ('HTTPS/REST', 'HTTPS/REST'), 'jetty': ('endpoint REST exposto pelo TIE', 'endpoint REST expuesto por el TIE'),
    'mllp': ('HL7 v2 sobre MLLP (TCP)', 'HL7 v2 sobre MLLP (TCP)'), 'cxf': ('Web service SOAP', 'Web service SOAP'),
    'file': ('troca de arquivos em pasta', 'intercambio de archivos en carpeta'), 'ftp': ('FTP', 'FTP'), 'sftp': ('SFTP', 'SFTP'),
    'kafka': ('mensageria Kafka', 'mensajería Kafka'), 'netty4': ('TCP (Netty)', 'TCP (Netty)'),
    'scheduler': ('execução agendada (scheduler)', 'ejecución programada (scheduler)'),
}
TRANSFORMACOES = {'json-json': 'JSON → JSON', 'xml-json': 'XML → JSON', 'hl7-json': 'HL7 → JSON', 'json-hl7': 'JSON → HL7',
                  'hl7-xml': 'HL7 → XML', 'xslt': 'XSLT', 'templates': 'template'}
PESSOAIS = {'PESSOA_FISICA', 'COMPL_PESSOA_FISICA', 'PF_CODIGO_EXTERNO', 'PACIENTE', 'ATENDIMENTO_PACIENTE', 'PESSOA_FISICA_AUX',
            'AGENDA_PACIENTE', 'AGENDA_CONSULTA', 'PRESCR_MEDICA', 'EXAME_LAB_RESULTADO', 'LAUDO_PACIENTE', 'EVOLUCAO_PACIENTE'}


def _t(idioma, pt, es):
    return pt if idioma == 'pt-BR' else es


def _esquema(uri):
    return re.split(r'[:/]', uri)[0].lower()


def _sim(idioma, v):
    return _t(idioma, 'Sim', 'Sí') if v else _t(idioma, 'Não', 'No')


# ------------------------------------------------------------------ Manual de integração TIE
def manual_tie(idx, arquivo, idioma, nome=None, cliente=None):
    b = idx.tie(arquivo)
    if not b:
        raise ValueError(f'integração TIE não encontrada no catálogo: {arquivo} (use buscar_tie)')
    L = lambda pt, es: _t(idioma, pt, es)
    integ = b['integracoes'][0] if b['integracoes'] else {}
    nome = nome or integ.get('nome') or b['integracao']
    bft = b['arquivo'].split('/')[-1]
    esquemas = sorted({_esquema(u) for x in b['fluxos'] + b['conectores'] for u in x['uris']})
    formas = [ESQUEMAS[e][0 if idioma == 'pt-BR' else 1] for e in esquemas if e in ESQUEMAS]
    transf = sorted({TRANSFORMACOES[e] for e in esquemas if e in TRANSFORMACOES})
    apis = sorted({a for f in b['fluxos'] for a in f['apis_tasy']})
    entrada = [c for c in b['conectores'] if any(_esquema(u) in ('jetty', 'mllp', 'cxf', 'netty4') for u in c['uris'])]
    saida = [e for e in b['eventos'] if e.get('gatilhos')]
    tabelas = sorted({g['tabela_trigger'] for e in b['eventos'] for g in e.get('gatilhos', []) if g.get('tabela_trigger')})
    pend = L('PREENCHER', 'COMPLETAR')

    # 1 Objetivo
    descr = integ.get('descricao') or ''
    objetivo = [{'tipo': 'paragrafo', 'revisar': True, 'texto': L(
        f'Esta integração conecta o Tasy ao sistema externo por meio do Tasy Interface Engine (TIE), usando o pacote `{bft}`.',
        f'Esta integración conecta Tasy con el sistema externo por medio del Tasy Interface Engine (TIE), usando el paquete `{bft}`.')}]
    if descr:
        objetivo.append({'tipo': 'paragrafo', 'revisar': True, 'texto': L('Descrição no catálogo TIE: ', 'Descripción en el catálogo TIE: ') + descr})
    objetivo.append({'tipo': 'preencher', 'texto': L('necessidade do cliente e problema que a integração resolve',
                                                    'necesidad del cliente y problema que la integración resuelve')})
    carac = []
    for r in b['rotas']:
        fl = next((f for f in b['fluxos'] if f['nome'] == r['fluxo']), {})
        ev = next((e for e in b['eventos'] if e['nome'] == r['evento']), {})
        carac.append(L(f"Evento `{r['evento']}`: ", f"Evento `{r['evento']}`: ") + (ev.get('descricao') or fl.get('descricao') or f'[{pend}: {L("o que este evento faz", "qué hace este evento")}]'))
    # 1.3 dados pessoais
    sens = [t for t in tabelas if t in PESSOAIS]
    dados = [{'tipo': 'paragrafo', 'revisar': True, 'texto': L(
        'A integração trafega dados de: ' + ', '.join(f'`{t}`' for t in sens) + '. Confirmar quais campos pessoais ou sensíveis são enviados.',
        'La integración transmite datos de: ' + ', '.join(f'`{t}`' for t in sens) + '. Confirmar qué campos personales o sensibles se envían.')}] if sens else \
        [{'tipo': 'preencher', 'texto': L('dados pessoais e sensíveis exportados/importados (o catálogo TIE não informa os campos)',
                                          'datos personales y sensibles exportados/importados (el catálogo TIE no informa los campos)')}]
    # 2 requisitos
    infra = [L('Tasy Interface Engine (TIE) instalado e em execução no ambiente do cliente.', 'Tasy Interface Engine (TIE) instalado y en ejecución en el ambiente del cliente.')]
    if apis:
        infra.append(L('Tasy Interfaces (APIs do Tasy) acessível pelo TIE.', 'Tasy Interfaces (APIs de Tasy) accesible desde el TIE.'))
    if entrada:
        infra.append(L('Porta do conector do TIE liberada para o sistema externo.', 'Puerto del conector del TIE liberado para el sistema externo.'))
    if any(_esquema(u) in ('http4', 'https4', 'mllp', 'ftp', 'sftp') and 'tasy-interfaces' not in u for f in b['fluxos'] for u in f['uris']):
        infra.append(L('Conectividade de rede do TIE até o endereço do sistema externo.', 'Conectividad de red del TIE hacia la dirección del sistema externo.'))
    infra.append(f'[{pend}: ' + L('servidores, portas, certificados e ambientes', 'servidores, puertos, certificados y ambientes') + ']')
    sistema = [L(f'Importar o pacote `{bft}` no TIE.', f'Importar el paquete `{bft}` en el TIE.')]
    if tabelas:
        sistema.append(L('Eventos disparados por gatilhos do Tasy nas tabelas: ', 'Eventos disparados por triggers de Tasy en las tablas: ') + ', '.join(f'`{t}`' for t in tabelas) + '.')
    sistema.append(f'[{pend}: ' + L('cadastros e funções do Tasy necessários', 'registros y funciones de Tasy necesarios') + ']')

    # 3 fluxo: um passo a passo por rota
    passos, modelo = [], None
    for r in b['rotas']:
        ev = next((e for e in b['eventos'] if e['nome'] == r['evento']), {'gatilhos': []})
        fl = next((f for f in b['fluxos'] if f['nome'] == r['fluxo']), {'uris': [], 'apis_tasy': [], 'metodos_http': []})
        gat = ev.get('gatilhos') or []
        if gat:
            g = gat[0]
            if g.get('inferido'):
                passos.append(f"[[{L('Gatilho inferido pelo nome, confirmar', 'Trigger inferido por el nombre, confirmar')}: `{g['objeto']}`]]")
            passos.append(L(f"No Tasy, `{g['objeto']}`" + (f" (tabela `{g['tabela_trigger']}`)" if g.get('tabela_trigger') else '') + f" dispara o evento `{r['evento']}`.",
                            f"En Tasy, `{g['objeto']}`" + (f" (tabla `{g['tabela_trigger']}`)" if g.get('tabela_trigger') else '') + f" dispara el evento `{r['evento']}`."))
        elif [c for c in entrada if c['nome'] in (r['evento'], r['nome'], r['fluxo'])] or (entrada and len(b['rotas']) == 1):
            passos.append(L(f"O sistema externo chama o conector `{entrada[0]['nome']}` do TIE, que gera o evento `{r['evento']}`.",
                            f"El sistema externo llama al conector `{entrada[0]['nome']}` del TIE, que genera el evento `{r['evento']}`."))
        else:
            passos.append(f"[{pend}: " + L(f"o que dispara o evento `{r['evento']}` no Tasy", f"qué dispara el evento `{r['evento']}` en Tasy") + ']')
        passos.append(L(f"A rota `{r['nome']}` do TIE recebe o evento e executa o fluxo `{r['fluxo']}`.",
                        f"La ruta `{r['nome']}` del TIE recibe el evento y ejecuta el flujo `{r['fluxo']}`."))
        if fl['apis_tasy']:
            passos.append(L('O fluxo chama as APIs do Tasy: ', 'El flujo llama a las APIs de Tasy: ') + ', '.join(f'`{a}`' for a in fl['apis_tasy'][:8]) + '.')
        else:
            met = '/'.join(fl['metodos_http']) or 'envio'
            passos.append(L(f'O fluxo transforma a mensagem e envia ao sistema externo ({met}).', f'El flujo transforma el mensaje y lo envía al sistema externo ({met}).'))
        if modelo is None:
            ext = L('Sistema externo', 'Sistema externo')
            if gat or not entrada:
                nos = [('i', 'inicio', 'Tasy', L('Início', 'Inicio')), ('t1', 'tarefa', 'Tasy', L('Usuário executa a ação no Tasy', 'Usuario ejecuta la acción en Tasy')),
                       ('t2', 'tarefa', 'Tasy', L(f"Gatilho dispara {r['evento']}", f"Trigger dispara {r['evento']}")),
                       ('t3', 'tarefa', 'TIE', L('Rota executa o fluxo e transforma', 'Ruta ejecuta el flujo y transforma')),
                       ('t4', 'tarefa', ext, L('Recebe a mensagem', 'Recibe el mensaje')), ('f', 'fim', ext, L('Fim', 'Fin'))]
            else:
                nos = [('i', 'inicio', ext, L('Início', 'Inicio')), ('t1', 'tarefa', ext, L('Envia a requisição', 'Envía la solicitud')),
                       ('t2', 'tarefa', 'TIE', L('Conector recebe e roteia', 'Conector recibe y enruta')),
                       ('t3', 'tarefa', 'TIE', L('Fluxo transforma e chama a API', 'Flujo transforma y llama a la API')),
                       ('t4', 'tarefa', 'Tasy', L('API do Tasy processa', 'API de Tasy procesa')), ('f', 'fim', 'Tasy', L('Fim', 'Fin'))]
            raias = ['Tasy', 'TIE', ext] if gat or not entrada else [ext, 'TIE', 'Tasy']
            modelo = {'tipo': 'bpmn', 'titulo': L(f'Fluxo da integração {nome}', f'Flujo de la integración {nome}'), 'nome': 'fluxo-integracao', 'raias': raias,
                      'nos': [{'id': i, 'tipo': t, 'raia': ra, 'texto': tx} for i, t, ra, tx in nos],
                      'ligacoes': [{'de': a[0], 'para': c[0]} for a, c in zip(nos, nos[1:])]}
    fluxo = ([{'tipo': 'diagrama', 'modelo': modelo}] if modelo else []) + \
            [{'tipo': 'lista', 'numerada': True, 'revisar': True, 'itens': passos or [f'[{pend}: ' + L('passo a passo do processo', 'paso a paso del proceso') + ']']}]

    # 4.2 tabelas do TIE
    sem = '—'
    con = [[c['nome'], c['tipo'], '\n'.join(u for u in c['uris'] if not u.startswith('direct:')) or sem, c.get('descricao') or sem] for c in b['conectores']]
    evs = [[e['nome'], e.get('descricao') or f'[{pend}]',
            '\n'.join(sorted({('[[' + g['objeto'] + ']]') if g.get('inferido') else g['objeto'] for g in e.get('gatilhos', [])})) or sem,
            ', '.join(sorted({g['tabela_trigger'] for g in e.get('gatilhos', []) if g.get('tabela_trigger')})) or sem,
            ', '.join(sorted({(g.get('payload') or '').rstrip('(') for g in e.get('gatilhos', []) if g.get('payload')})) or sem] for e in b['eventos']]
    def curto(itens, n=3):
        itens = list(dict.fromkeys(itens))
        return '\n'.join(itens[:n]) + (f'\n(+{len(itens) - n}, ' + L('lista abaixo', 'lista abajo') + ')' if len(itens) > n else '') or sem

    fls = [[f['nome'], f.get('descricao') or f'[{pend}]', curto([u for u in f['uris'] if _esquema(u) in ESQUEMAS]),
            ', '.join(f['metodos_http']) or sem, curto(f['apis_tasy'])] for f in b['fluxos']]
    listas_fl = []
    for f in b['fluxos']:
        if len(set(f['apis_tasy'])) > 3:
            listas_fl += [{'tipo': 'subtitulo', 'texto': L(f"APIs do Tasy chamadas pelo fluxo {f['nome']}", f"APIs de Tasy llamadas por el flujo {f['nome']}")},
                          {'tipo': 'lista', 'itens': [f'`{a}`' for a in dict.fromkeys(f['apis_tasy'])]}]
    rts = [[r['nome'], r['evento'], r['fluxo'], _sim(idioma, r['ativa']), r.get('condicao') or sem, r.get('versao_min') or sem] for r in b['rotas']]
    params = sorted({m for x in b['fluxos'] + b['conectores'] for u in x['uris'] for m in re.findall(r'\{(host|cfg)\}', u)})

    def tab(colunas, linhas, vazio):
        return [{'tipo': 'tabela', 'colunas': colunas, 'linhas': linhas}] if linhas else [{'tipo': 'paragrafo', 'texto': vazio}]

    secoes = [
        {'id': '1', 'nivel': 1, 'titulo': L(f'Objetivo da integração {nome}', f'Objetivo de la integración {nome}'), 'blocos': objetivo},
        {'id': '1.1', 'nivel': 2, 'titulo': L('Principais características', 'Principales características'),
         'blocos': [{'tipo': 'lista', 'revisar': True, 'itens': carac or [f'[{pend}]']}]},
        {'id': '1.2', 'nivel': 2, 'titulo': 'Público', 'blocos': [{'tipo': 'preencher', 'texto': L('profissionais e áreas que usam a integração', 'profesionales y áreas que usan la integración')}]},
        {'id': '1.3', 'nivel': 2, 'titulo': L('Dados pessoais e sensíveis', 'Datos personales y sensibles'), 'blocos': dados},
        {'id': '2', 'nivel': 1, 'titulo': L(f'Requisitos necessários para a integração {nome}', f'Requerimientos necesarios para la integración {nome}'),
         'blocos': [L('Abaixo estão os requisitos mínimos de infraestrutura e de sistema para a integração funcionar.',
                      'A continuación se describen los requisitos mínimos de infraestructura y de sistema para que la integración funcione.')]},
        {'id': '2.1', 'nivel': 2, 'titulo': L('Infraestrutura', 'Infraestructura'), 'blocos': [{'tipo': 'lista', 'itens': infra}]},
        {'id': '2.2', 'nivel': 2, 'titulo': 'Sistema', 'blocos': [{'tipo': 'lista', 'itens': sistema}]},
        {'id': '3', 'nivel': 1, 'titulo': L(f'Fluxo da integração {nome}', f'Flujo de la integración {nome}'), 'blocos': fluxo},
        {'id': '4', 'nivel': 1, 'titulo': L('Configurações e parametrizações no sistema', 'Configuraciones y parametrizaciones en el sistema'),
         'blocos': [L('Abaixo estão as configurações necessárias no Tasy Interface Engine (TIE) e no Tasy.',
                      'A continuación se describen las configuraciones necesarias en el Tasy Interface Engine (TIE) y en Tasy.')]},
        {'id': '4.1', 'nivel': 2, 'titulo': L('Forma de comunicação', 'Forma de comunicación'), 'blocos': [
            {'tipo': 'paragrafo', 'texto': L('Comunicação: ', 'Comunicación: ') + ('; '.join(dict.fromkeys(formas)) or f'[{pend}]') + '.' +
                (L(' Transformações usadas: ', ' Transformaciones usadas: ') + ', '.join(transf) + '.' if transf else '')}]},
        {'id': '4.2', 'nivel': 2, 'titulo': L('Cadastros e parametrizações', 'Registros y parametrizaciones'), 'blocos': [
            L(f'Os artefatos abaixo fazem parte do pacote `{bft}` (integração `{b["integracao"]}` do catálogo TIE).',
              f'Los artefactos siguientes forman parte del paquete `{bft}` (integración `{b["integracao"]}` del catálogo TIE).'),
            {'tipo': 'lista', 'numerada': True, 'itens': [
                L(f'No TIE, importar o arquivo `{bft}`.', f'En el TIE, importar el archivo `{bft}`.'),
                L('Conferir se conector, eventos, fluxos, rotas e mapeamentos foram criados.', 'Verificar que conector, eventos, flujos, rutas y mapeos fueron creados.'),
                L('Configurar endereços e credenciais do ambiente (itens em amarelo abaixo).', 'Configurar direcciones y credenciales del ambiente (ítems en amarillo abajo).'),
                L('Ativar as rotas necessárias.', 'Activar las rutas necesarias.')]}]},
        {'id': '4.2.1', 'nivel': 3, 'titulo': 'Conector', 'blocos': tab([L('Nome', 'Nombre'), L('Tipo', 'Tipo'), 'Endpoint', L('Descrição', 'Descripción')], con,
                                                                         L('Este pacote não traz conector próprio: os fluxos são acionados por eventos do Tasy.',
                                                                           'Este paquete no trae conector propio: los flujos son accionados por eventos de Tasy.'))},
        {'id': '4.2.2', 'nivel': 3, 'titulo': 'Evento', 'blocos': tab(['Evento', L('Descrição', 'Descripción'), L('Gatilho no Tasy', 'Trigger en Tasy'),
                                                                       L('Tabela de origem', 'Tabla de origen'), L('Montagem do payload', 'Montaje del payload')], evs, f'[{pend}]')},
        {'id': '4.2.3', 'nivel': 3, 'titulo': L('Fluxo', 'Flujo'), 'blocos': tab([L('Fluxo', 'Flujo'), L('Descrição', 'Descripción'), L('Destinos', 'Destinos'),
                                                                                  L('Método', 'Método'), L('APIs do Tasy chamadas', 'APIs de Tasy llamadas')], fls, f'[{pend}]') + listas_fl},
        {'id': '4.2.4', 'nivel': 3, 'titulo': L('Rota', 'Ruta'), 'blocos': tab([L('Rota', 'Ruta'), 'Evento', L('Fluxo', 'Flujo'), L('Ativa no pacote', 'Activa en el paquete'),
                                                                                L('Condição', 'Condición'), L('Versão mín. Tasy Interfaces', 'Versión mín. Tasy Interfaces')], rts, f'[{pend}]') +
            ([{'tipo': 'paragrafo', 'revisar': True, 'texto': L('Há rotas que vêm desativadas no pacote: ativar as que o cliente usa.',
                                                                'Hay rutas que vienen desactivadas en el paquete: activar las que el cliente utiliza.')}] if any(not r['ativa'] for r in b['rotas']) else [])},
        {'id': '4.2.5', 'nivel': 3, 'titulo': L('Mapeamento', 'Mapeo'), 'blocos': (
            [{'tipo': 'tabela', 'colunas': [L('Mapeamento', 'Mapeo'), L('De-para (origem → destino)', 'De-para (origen → destino)')],
              'linhas': [[m, f'[{pend}: ' + L('campos de origem e destino', 'campos de origen y destino') + ']'] for m in b['mapeamentos']]}]
            if b['mapeamentos'] else [L('Este pacote não usa mapeamentos.', 'Este paquete no usa mapeos.')])},
        {'id': '4.2.6', 'nivel': 3, 'titulo': L('Parâmetros do Tasy', 'Parámetros de Tasy'), 'blocos': [
            {'tipo': 'tabela', 'colunas': [L('Parâmetro', 'Parámetro'), L('Onde', 'Dónde'), L('Valor', 'Valor')], 'linhas':
                ([[L('Endereço (host) do sistema externo / do Tasy Interfaces', 'Dirección (host) del sistema externo / de Tasy Interfaces'), L('Fluxos e conector do TIE', 'Flujos y conector del TIE'),
                   f'[{pend}: ' + L('por ambiente', 'por ambiente') + ']']] if 'host' in params else []) +
                ([[L('Porta, caminho e credenciais', 'Puerto, ruta y credenciales'), L('Propriedades do pacote no TIE', 'Propiedades del paquete en el TIE'),
                   f'[{pend}: ' + L('por ambiente; nunca registrar senhas neste manual', 'por ambiente; nunca registrar contraseñas en este manual') + ']']] if 'cfg' in params else []) +
                [[L('Parâmetros e cadastros funcionais do Tasy', 'Parámetros y registros funcionales de Tasy'), L('Funções do Tasy', 'Funciones de Tasy'), f'[{pend}]']]}]},
        {'id': '5', 'nivel': 1, 'titulo': L(f'Testes da integração {nome}', f'Pruebas de la integración {nome}'), 'blocos': []},
        {'id': '5.1', 'nivel': 2, 'titulo': L('Processo', 'Proceso'), 'blocos': [{'tipo': 'lista', 'numerada': True, 'revisar': True, 'itens': [
            L(f"Executar no Tasy a ação que gera o evento `{r['evento']}` e conferir a execução da rota `{r['nome']}` no monitor do TIE.",
              f"Ejecutar en Tasy la acción que genera el evento `{r['evento']}` y verificar la ejecución de la ruta `{r['nome']}` en el monitor del TIE.") if saida else
            L(f"Enviar uma requisição de teste ao conector e conferir a execução da rota `{r['nome']}` no monitor do TIE.",
              f"Enviar una solicitud de prueba al conector y verificar la ejecución de la ruta `{r['nome']}` en el monitor del TIE.")
            for r in b['rotas'][:12]] or [f'[{pend}]']}]},
        {'id': '5.2', 'nivel': 2, 'titulo': L('Visualização dos resultados', 'Visualización de resultados'), 'blocos': [
            {'tipo': 'preencher', 'texto': L('telas do Tasy e logs do TIE onde o resultado aparece (incluir imagens)', 'pantallas de Tasy y logs del TIE donde aparece el resultado (incluir imágenes)')}]},
    ]
    titulo = L(f'Integração {nome}', f'Integración {nome}')
    return {'tipo': 'manual', 'idioma': idioma, 'capa': {'titulo': titulo, 'cliente': cliente or ''}, 'secoes': secoes,
            'fonte': {'bft': b['arquivo'], 'readme': b.get('readme', '')}}


# ------------------------------------------------------------------ Manual de API (modelo "MI - API Atendimentos")
def manual_api(idx, api, idioma, nome=None):
    """api: título da API no Swagger (ex.: 'Schedules') ou nome do arquivo (ex.: 'schedules_1.json')."""
    L = lambda pt, es: _t(idioma, pt, es)
    alvo = api.lower()
    ops = [o for o in idx.ops if o['api'].lower() == alvo or alvo in o['arquivo'].lower().split(', ')]
    if not ops:
        raise ValueError(f'API não encontrada nos Swaggers: {api} (use buscar_apis)')
    nome = nome or ops[0]['api']
    pend = L('PREENCHER', 'COMPLETAR')
    tabelas = sorted({t for o in ops for t in o['_tabs']})
    secoes = [
        {'id': '1', 'nivel': 1, 'titulo': L(f'Objetivo da integração {nome}', f'Objetivo de la integración {nome}'), 'blocos': [
            {'tipo': 'paragrafo', 'revisar': True, 'texto': L(
                f'Este manual descreve a API padrão **{nome}** do Tasy (Tasy Interfaces), com {len(ops)} operações, para integração com sistemas externos.',
                f'Este manual describe la API estándar **{nome}** de Tasy (Tasy Interfaces), con {len(ops)} operaciones, para integración con sistemas externos.')}]},
        {'id': '1.1', 'nivel': 2, 'titulo': L('Principais características', 'Principales características'),
         'blocos': [{'tipo': 'lista', 'itens': [f"`{o['metodo']} {o['path']}` — {o['resumo'][:140]}" for o in ops]}]},
        {'id': '1.2', 'nivel': 2, 'titulo': 'Público', 'blocos': [{'tipo': 'preencher', 'texto': L('equipes que consomem a API', 'equipos que consumen la API')}]},
        {'id': '1.3', 'nivel': 2, 'titulo': L('Dados pessoais e sensíveis', 'Datos personales y sensibles'), 'blocos': [
            {'tipo': 'paragrafo', 'revisar': True, 'texto': L('Tabelas do Tasy expostas pela API: ', 'Tablas de Tasy expuestas por la API: ') + ', '.join(f'`{t}`' for t in tabelas[:25]) +
             L('. Tabelas com dados pessoais: ', '. Tablas con datos personales: ') + (', '.join(f'`{t}`' for t in tabelas if t in PESSOAIS) or '—') + '.'}]},
        {'id': '2', 'nivel': 1, 'titulo': L(f'Requisitos necessários para a integração {nome}', f'Requerimientos necesarios para la integración {nome}'), 'blocos': []},
        {'id': '2.1', 'nivel': 2, 'titulo': L('Infraestrutura', 'Infraestructura'), 'blocos': [{'tipo': 'lista', 'itens': [
            L('Tasy Interfaces instalado e acessível pelo sistema externo (diretamente ou pelo TIE).', 'Tasy Interfaces instalado y accesible para el sistema externo (directamente o por el TIE).'),
            f'[{pend}: ' + L('URL base por ambiente, autenticação e versão mínima do Tasy', 'URL base por ambiente, autenticación y versión mínima de Tasy') + ']']}]},
        {'id': '2.2', 'nivel': 2, 'titulo': 'Sistema', 'blocos': [{'tipo': 'preencher', 'texto': L('cadastros e permissões do Tasy necessários', 'registros y permisos de Tasy necesarios')}]},
        {'id': '3', 'nivel': 1, 'titulo': L(f'Fluxo da integração {nome}', f'Flujo de la integración {nome}'), 'blocos': [
            {'tipo': 'diagrama', 'modelo': {'tipo': 'sequencia', 'nome': 'fluxo-api', 'titulo': L(f'Chamada à API {nome}', f'Llamada a la API {nome}'),
                                            'participantes': [L('Sistema externo', 'Sistema externo'), 'Tasy Interfaces', 'Tasy'],
                                            'mensagens': [{'de': L('Sistema externo', 'Sistema externo'), 'para': 'Tasy Interfaces', 'texto': L('Requisição HTTP + token', 'Solicitud HTTP + token')},
                                                          {'de': 'Tasy Interfaces', 'para': 'Tasy', 'texto': L('Valida e executa', 'Valida y ejecuta')},
                                                          {'de': 'Tasy', 'para': 'Tasy Interfaces', 'texto': L('Dados / confirmação', 'Datos / confirmación'), 'retorno': True},
                                                          {'de': 'Tasy Interfaces', 'para': L('Sistema externo', 'Sistema externo'), 'texto': L('Resposta JSON', 'Respuesta JSON'), 'retorno': True}]}}]},
        {'id': '4', 'nivel': 1, 'titulo': L('Configurações e parametrizações no sistema', 'Configuraciones y parametrizaciones en el sistema'), 'blocos': []},
        {'id': '4.1', 'nivel': 2, 'titulo': L('Forma de comunicação', 'Forma de comunicación'), 'blocos': ['HTTP/REST (JSON).']},
        {'id': '4.2', 'nivel': 2, 'titulo': L('Cadastros e parametrizações', 'Registros y parametrizaciones'), 'blocos': [
            L('Cada operação abaixo traz os campos (tags JSON) e a tabela e o campo do Tasy correspondentes, conforme o Swagger.',
              'Cada operación a continuación trae los campos (tags JSON) y la tabla y el campo de Tasy correspondientes, según el Swagger.')]},
    ]
    for o in ops:
        secoes.append({'id': f"4.2.{o['metodo']} {o['path']}", 'nivel': 3, 'titulo': f"{o['metodo']} {o['path']}", 'blocos': [
            o['resumo'] or f'[{pend}]'] + _campos_api(o, idioma)})
    secoes += [
        {'id': '5', 'nivel': 1, 'titulo': L(f'Testes da integração {nome}', f'Pruebas de la integración {nome}'), 'blocos': []},
        {'id': '5.1', 'nivel': 2, 'titulo': L('Processo', 'Proceso'), 'blocos': [{'tipo': 'preencher', 'texto': L('roteiro de teste por operação (ex.: coleção Postman)', 'guion de prueba por operación (ej.: colección Postman)')}]},
        {'id': '5.2', 'nivel': 2, 'titulo': L('Visualização dos resultados', 'Visualización de resultados'), 'blocos': [{'tipo': 'preencher', 'texto': L('onde conferir o resultado no Tasy', 'dónde verificar el resultado en Tasy')}]},
    ]
    return {'tipo': 'manual', 'idioma': idioma, 'capa': {'titulo': L(f'API {nome}', f'API {nome}')}, 'secoes': secoes,
            'fonte': {'swagger': sorted({o['arquivo'] for o in ops})}}


def _campos_api(o, idioma, limite=60):
    L = lambda pt, es: _t(idioma, pt, es)
    onde = {'path': L('caminho', 'ruta'), 'query': L('filtro', 'filtro'), 'header': L('cabeçalho', 'encabezado'), 'corpo': L('corpo', 'cuerpo'), 'resposta': L('resposta', 'respuesta')}
    blocos = []
    for grupo, titulo in ((('path', 'query', 'header', 'corpo'), L('Entrada', 'Entrada')), (('resposta',), L('Resposta', 'Respuesta'))):
        campos = [c for c in o['campos'] if c['em'] in grupo]
        if not campos:
            continue
        linhas = [[c['nome'], onde.get(c['em'], c['em']), c['tipo'], _sim(idioma, c['obrigatorio']) if c['em'] != 'resposta' else '—',
                   c['tabela'] or '—', c['coluna'] or '—', c['descricao'][:90]] for c in campos[:limite]]
        blocos.append({'tipo': 'subtitulo', 'texto': f'{titulo} — ' + L('mapeamento das tags JSON', 'mapeo de las tags JSON')})
        blocos.append({'tipo': 'tabela', 'colunas': ['Tag JSON', L('Onde', 'Dónde'), L('Tipo', 'Tipo'), L('Obrig.', 'Oblig.'), L('Tabela Tasy', 'Tabla Tasy'),
                                                     L('Campo Tasy', 'Campo Tasy'), L('Descrição', 'Descripción')], 'linhas': linhas,
                       'larguras': [20, 7, 10, 5, 21, 19, 18]})
        if len(campos) > limite:
            blocos.append({'tipo': 'paragrafo', 'revisar': True, 'texto': L(f'Mostrados {limite} de {len(campos)} campos; a lista completa está no Swagger.',
                                                                            f'Mostrados {limite} de {len(campos)} campos; la lista completa está en el Swagger.')})
    return blocos


# ------------------------------------------------------------------ LI
def li(reqs, classes, idioma, capa=None, sistema_terceiro='', idx=None):
    """Rascunho de LI a partir dos requisitos extraídos e da classificação (um caso de uso por requisito)."""
    L = lambda pt, es: _t(idioma, pt, es)
    pend = L('PREENCHER', 'COMPLETAR')
    terceiro = sistema_terceiro or (capa or {}).get('software') or f'[{pend}: sistema]'
    cus = []
    for n, (r, c) in enumerate(zip(reqs, classes), 1):
        escrita = r.get('operacao') == 'escrita'
        cus.append({'id': f'CU{n:02d}', 'req': r, 'cls': c, 'direcao': f'{terceiro} → Tasy' if escrita else f'Tasy → {terceiro}',
                    'area': r.get('grupo', '')})
    via_tie = any(x['cls']['classe'] == 'TIE' for x in cus)
    S = []

    def sec(i, nivel, titulo, blocos, **kw):
        S.append({'id': i, 'nivel': nivel, 'titulo': titulo, 'blocos': blocos, **kw})

    sec('1', 1, L('Objetivo – Propósito do documento', 'Objetivo – Propósito del documento'), [L(
        f'Este documento especifica os requisitos e processos da integração entre o Tasy e o {terceiro}' + (', com o Tasy Interface Engine (TIE) como middleware.' if via_tie else '.'),
        f'Este documento especifica los requerimientos y procesos de la integración entre Tasy y {terceiro}' + (', con el Tasy Interface Engine (TIE) como middleware.' if via_tie else '.'))])
    sec('1.1', 2, L('Formato de comunicação e método', 'Formato de comunicación y método'), [
        {'tipo': 'tabela', 'revisar': True, 'colunas': [L('Trecho (origem - destino)', 'Tramo (origen - destino)'), L('Formato / protocolo', 'Formato / protocolo')],
         'linhas': [[f'{terceiro} - Tasy Interfaces', 'HTTP/REST (JSON)']] + ([[f'{terceiro} - TIE - Tasy', f'[{pend}: ' + L('protocolo do trecho TIE', 'protocolo del tramo TIE') + ']']] if via_tie else [])}])
    sec('1.2', 2, L('Descrição dos sistemas (principais funcionalidades)', 'Descripción de los sistemas (principales funcionalidades)'), [
        {'tipo': 'preencher', 'texto': L('um parágrafo por sistema: Tasy (funções envolvidas), TIE (se houver) e sistema terceiro', 'un párrafo por sistema: Tasy (funciones involucradas), TIE (si aplica) y sistema tercero')}])
    areas = sorted({x['area'] for x in cus if x['area']})
    sec('2', 1, L('Escopo e responsabilidades', 'Alcance y responsabilidades'), [
        {'tipo': 'paragrafo', 'revisar': True, 'texto': L(f'A integração cobre {len(cus)} pontos de integração' + (f" nas áreas: {', '.join(areas)}." if areas else '.'),
                                                          f'La integración cubre {len(cus)} puntos de integración' + (f" en las áreas: {', '.join(areas)}." if areas else '.'))},
        {'tipo': 'tabela', 'revisar': True, 'colunas': [L('Parte', 'Parte'), L('Responsabilidade principal', 'Responsabilidad principal')],
         'linhas': [['Bionexo Tasy', f'[{pend}]'], [L('Cliente', 'Cliente'), f'[{pend}]'], [terceiro, f'[{pend}]']]}])
    sec('3', 1, L('Objetivos e descrição geral dos requisitos', 'Objetivos y descripción general de los requerimientos'), [
        {'tipo': 'preencher', 'texto': L('fluxo de negócio em texto corrido, citando os casos de uso na ordem em que acontecem', 'flujo de negocio en texto corrido, citando los casos de uso en el orden en que ocurren')}])
    sec('3.1', 2, L('Objetivo da integração / Principais características', 'Objetivo de la integración / Principales características'), [{'tipo': 'preencher', 'texto': L('lista de características', 'lista de características')}])
    sec('3.2', 2, L('Casos de uso / Pontos de integração', 'Casos de uso / Puntos de integración'), [
        {'tipo': 'diagrama', 'modelo': {'tipo': 'casos_de_uso', 'nome': 'casos-de-uso', 'titulo': L('Casos de uso', 'Casos de uso'), 'sistema': f'Tasy x {terceiro}',
                                        'atores': [terceiro, {'nome': 'Tasy', 'lado': 'direita'}],
                                        'casos': [{'nome': f"{x['id']} – {x['req']['nome']}"[:60], 'atores': [terceiro, 'Tasy']} for x in cus[:12]]}},
        *([{'tipo': 'paragrafo', 'revisar': True, 'texto': L(f'O diagrama mostra os 12 primeiros casos de uso; a tabela abaixo lista os {len(cus)}.', f'El diagrama muestra los 12 primeros casos de uso; la tabla siguiente lista los {len(cus)}.')}] if len(cus) > 12 else []),
        {'tipo': 'tabela', 'colunas': ['ID', L('Área', 'Área'), L('Caso de uso', 'Caso de uso'), L('Direção', 'Dirección')],
         'linhas': [[x['id'], x['area'], x['req']['nome'], x['direcao']] for x in cus], 'larguras': [6, 16, 34, 18]}])
    sec('3.3', 2, L('Requisitos funcionais (regras de negócio)', 'Requerimientos funcionales (reglas de negocio)'), [
        {'tipo': 'tabela', 'revisar': True, 'colunas': [L('Regra (RN-xx)', 'Regla (RN-xx)'), L('Descrição', 'Descripción')], 'linhas': [['RN-01', f'[{pend}]']]}])
    sec('3.4', 2, L('Requisitos não funcionais', 'Requerimientos no funcionales'), [{'tipo': 'preencher', 'texto': L('disponibilidade, logs, portas, volumetria', 'disponibilidad, logs, puertos, volumetría')}])
    sec('3.5', 2, L('Premissas', 'Premisas'), [{'tipo': 'lista', 'revisar': True, 'itens': [
        L('O terceiro deixa de acessar o banco do Tasy diretamente e passa a usar os contratos descritos nesta LI.', 'El tercero deja de acceder directamente a la base de Tasy y pasa a usar los contratos descritos en esta LI.')]}])
    sec('3.6', 2, L('Requisitos necessários para a integração', 'Requerimientos necesarios para la integración'), [{'tipo': 'preencher', 'texto': L('cadastros, parametrizações e componentes instalados', 'registros, parametrizaciones y componentes instalados')}])
    sec('4', 1, L('Especificações de arquitetura / sistema', 'Especificaciones de arquitectura / sistema'), [{'tipo': 'preencher', 'texto': L('diagrama do ambiente do cliente e versão do Tasy', 'diagrama del ambiente del cliente y versión de Tasy')}])
    sec('5', 1, L('Processos de negócio (mapa)', 'Procesos de negocio (mapa)'), [{'tipo': 'preencher', 'texto': L('mapa do processo (BPMN com raias por ator)', 'mapa del proceso (BPMN con carriles por actor)')}])
    sec('6', 1, L('Detalhamento da integração por caso de uso', 'Detalle de la integración por caso de uso'), [])
    for x in cus:
        r, c = x['req'], x['cls']
        contrato = f"`{c['api']}`" if c['classe'] in ('OpenAPI', 'Parcial') and c.get('api') else ('TIE' if c['classe'] == 'TIE' else f'[{pend}]')
        tecnicas = [L(f'Contrato Tasy proposto: {contrato}.', f'Contrato Tasy propuesto: {contrato}.')]
        if c['confianca'] != 'Alta':  # só a conclusão incerta vai em amarelo; o que veio do documento do terceiro, não
            tecnicas[0] = f'[[{tecnicas[0]}]]'
        if r.get('procedures'):
            tecnicas.append(L('Procedures do Tasy envolvidas: ', 'Procedures de Tasy involucradas: ') + ', '.join(f'`{p}`' for p in r['procedures']) + '.')
        if r.get('filtros'):
            tecnicas.append(L('Filtros usados pelo terceiro: ', 'Filtros usados por el tercero: ') + (r['filtros'] if len(r['filtros']) <= 700 else r['filtros'][:700].rsplit(' ', 1)[0] + ' …'))
        sec(f"6.{x['id']}", 2, f"{x['id']} – {r['nome']}", [r.get('resumo') or f'[{pend}]'])
        sec(f"6.{x['id']}.gatilho", 3, L('Gatilho no Tasy', 'Disparador en Tasy'), [{'tipo': 'preencher', 'texto': L('ação que dispara a chamada', 'acción que dispara la llamada')}])
        sec(f"6.{x['id']}.telas", 3, L('Telas do Tasy', 'Pantallas de Tasy'), [{'tipo': 'preencher', 'texto': L('imagens das telas do processo', 'imágenes de las pantallas del proceso')}])
        sec(f"6.{x['id']}.fluxo", 3, L('Fluxo do processo', 'Flujo del proceso'), [{'tipo': 'diagrama', 'modelo': {
            'tipo': 'sequencia', 'nome': f"fluxo-{x['id'].lower()}", 'titulo': f"{x['id']} – {r['nome']}"[:70],
            'participantes': [terceiro] + (['TIE'] if c['classe'] == 'TIE' else []) + ['Tasy'],
            'mensagens': ([{'de': terceiro, 'para': 'TIE', 'texto': r.get('metodo', '') + ' ' + r['nome'][:28]}, {'de': 'TIE', 'para': 'Tasy', 'texto': L('consulta/procedure', 'consulta/procedure')},
                           {'de': 'Tasy', 'para': 'TIE', 'texto': L('dados', 'datos'), 'retorno': True}, {'de': 'TIE', 'para': terceiro, 'texto': 'JSON', 'retorno': True}]
                          if c['classe'] == 'TIE' else
                          [{'de': terceiro, 'para': 'Tasy', 'texto': (c.get('api') or r.get('metodo', ''))[:44]}, {'de': 'Tasy', 'para': terceiro, 'texto': L('resposta JSON', 'respuesta JSON'), 'retorno': True}])}}])
        sec(f"6.{x['id']}.tecnicas", 3, L('Especificações técnicas adicionais / regras de negócio', 'Especificaciones técnicas adicionales / reglas de negocio'),
            [{'tipo': 'lista', 'itens': tecnicas}])
    sec('7', 1, L('Layout e exemplo das mensagens', 'Layout y ejemplo de los mensajes'), [])
    for x in cus:
        r, c = x['req'], x['cls']
        linhas = []
        for n, d in enumerate(c.get('depara') or [], 1):
            tab, col = d['coluna'].split('.')
            linhas.append([n, d['campo_api'], '', '', tab, col, '', d['tipo'], '', ''])
        # sem cobertura: detalha só a tabela principal e as gravadas; tabelas de apoio (descrições, domínios) viram uma linha
        foco = {c.get('tabela_principal')} | set(r.get('tabelas_escrita') or {})
        faltam = c.get('colunas_sem_cobertura') or []
        for col in [f for f in faltam if f.split('.')[0] in foco]:
            tab, cl = col.split('.')
            linhas.append([len(linhas) + 1, f'[[{L("sem campo na API", "sin campo en la API")}]]', '', '', tab, cl, '', '', '', f'[[{L("ver seção 10", "ver sección 10")}]]'])
        apoio = sorted({f.split('.')[0] for f in faltam if f.split('.')[0] not in foco})
        nota = [{'tipo': 'paragrafo', 'revisar': True, 'texto': L(
            f'Além disso, o terceiro usa colunas de tabelas de apoio sem campo na API: {", ".join(apoio[:12])}{" …" if len(apoio) > 12 else ""} (detalhe na matriz interna).',
            f'Además, el tercero usa columnas de tablas de apoyo sin campo en la API: {", ".join(apoio[:12])}{" …" if len(apoio) > 12 else ""} (detalle en la matriz interna).')}] if apoio and c.get('api') else []
        sec(f"7.{x['id']}", 2, f"{x['id']} – {x['direcao']}: {r['nome']}", [])
        sec(f"7.{x['id']}.payload", 3, L('Layout do payload / mensagem', 'Layout del payload / mensaje'), [{'tipo': 'preencher', 'texto': L('exemplo real e anonimizado de envio e retorno', 'ejemplo real y anonimizado de envío y retorno')}])
        sec(f"7.{x['id']}.mapeamento", 3, L('Mapeamento das informações', 'Mapeo de la información'), [
            {'tipo': 'tabela', 'colunas': ['#', L('Campo do payload', 'Campo del payload'), L('Exemplo', 'Ejemplo'), L('Obrig.', 'Oblig.'), L('Tabela Tasy', 'Tabla Tasy'), L('Campo Tasy', 'Campo Tasy'),
                                           L('Aba/função no Tasy', 'Pestaña/función en Tasy'), L('Tipo', 'Tipo'), L('Tam.', 'Tam.'), L('Observações', 'Observaciones')],
             'linhas': linhas[:80], 'larguras': [3, 19, 8, 5, 16, 17, 9, 9, 4, 10]}] + nota if linhas else [{'tipo': 'preencher', 'texto': L('mapeamento dos campos', 'mapeo de los campos')}])
    sec('8', 1, L('Conexão e segurança', 'Conexión y seguridad'), [{'tipo': 'preencher', 'texto': L('certificados, HTTPS, tokens e validade, portas (nunca senhas)', 'certificados, HTTPS, tokens y vigencia, puertos (nunca contraseñas)')}])
    sec('9', 1, L('Abreviaturas e definições', 'Abreviaturas y definiciones'), [{'tipo': 'tabela', 'colunas': [L('Termo', 'Término'), L('Definição', 'Definición')], 'linhas': [
        ['API', L('Interface de programação de aplicações', 'Interfaz de programación de aplicaciones')], ['CU', L('Caso de uso', 'Caso de uso')],
        ['LI', L('Levantamento de Integração', 'Levantamiento de Integración')], ['TIE', 'Tasy Interface Engine'],
        ['Tasy Interfaces', L('Camada de APIs REST do Tasy', 'Capa de APIs REST de Tasy')], ['GAP', L('Funcionalidade não atendida pelo produto padrão', 'Funcionalidad no atendida por el producto estándar')]]}])
    gaps = [x for x in cus if x['cls']['classe'] in ('Gap', 'Parcial')]
    sec('10', 1, L('Lista de GAPs (produto)', 'Lista de GAPs (producto)'), [
        {'tipo': 'tabela', 'revisar': True, 'colunas': ['ID', 'Gap', L('Tipo', 'Tipo'), L('Prioridade', 'Prioridad'), L('Avaliação Philips EMR', 'Evaluación Philips EMR'), L('Nº do case', 'Nº del case'),
                                                        L('Responsável', 'Responsable'), L('Observação', 'Observación')],
         'linhas': [[f'GAP{n:02d}', f"{x['id']} – {x['req']['nome']}", L('Sem API/procedure', 'Sin API/procedure') if x['cls']['classe'] == 'Gap' else L('Campos sem cobertura na API', 'Campos sin cobertura en la API'),
                     '', '', '', '', (', '.join(x['cls'].get('colunas_sem_cobertura', [])[:6]) + (' …' if len(x['cls'].get('colunas_sem_cobertura', [])) > 6 else ''))]
                    for n, x in enumerate(gaps, 1)] or [['—', L('Nenhum gap identificado', 'Ningún gap identificado'), '', '', '', '', '', '']],
         'larguras': [6, 20, 13, 7, 9, 7, 9, 29]},
        {'tipo': 'paragrafo', 'texto': L('Legenda — Tipo: "Sem API/procedure" exige desenvolvimento; "Campos sem cobertura" pede ampliação de API existente ou complemento via TIE.',
                                         'Leyenda — Tipo: "Sin API/procedure" exige desarrollo; "Campos sin cobertura" pide ampliación de API existente o complemento vía TIE.')}])
    abertos = [x for x in cus if x['cls']['confianca'] == 'Baixa']
    sec('11', 1, L('Assuntos abertos e fechados', 'Asuntos abiertos y cerrados'), [
        {'tipo': 'tabela', 'revisar': True, 'colunas': ['ID', L('Assunto', 'Asunto'), L('Resolução / ação', 'Resolución / acción'), 'Status'],
         'linhas': [[f'A{n:02d}', L(f"{x['id']}: confirmar o contrato Tasy ({x['cls']['classe']})", f"{x['id']}: confirmar el contrato Tasy ({x['cls']['classe']})"), '', L('Aberto', 'Abierto')]
                    for n, x in enumerate(abertos, 1)] or [['—', '—', '', '']], 'larguras': [6, 40, 30, 10]}])
    sec('13', 1, L('Histórico de revisão', 'Historial de revisión'), [
        {'tipo': 'tabela', 'colunas': [L('Revisão', 'Revisión'), L('Data', 'Fecha'), L('Autor', 'Autor'), L('Descrição das mudanças', 'Descripción de los cambios'), L('CR / motivo', 'CR / motivo')],
         'linhas': [['1', f'[{pend}]', f'[{pend}]', L('Versão inicial', 'Versión inicial'), '—']]}])
    return {'tipo': 'li', 'idioma': idioma, 'capa': dict(capa or {}), 'secoes': S}
