# Modelo de LI (proposta para validação)

> Proposta para revisar com Angélica e Eberton. A estrutura em formato de máquina está em [`templates/li/estrutura.json`](../templates/li/estrutura.json).

## Bases analisadas

| Documento | O que é | O que aproveitamos |
|---|---|---|
| `templates/li/Template de levantamento de integração [OFICIAL].docx` | Template oficial (PT) com instruções por seção | Estrutura, nomes das seções, regras ("imagens obrigatórias", "fluxo visível", casos de teste) |
| `TecSalud - LI Integracion Baxter NCE` (ES, v1.6) | LI real, **entrada** no Tasy (terceiro → TIE), HL7 v2.6 | Seções extras que o template não tem e o nível de detalhe esperado: tabela de passo a passo por sistema, mapeamento com tabela/campo/aba/tipo/tamanho, exemplos de mensagem, regras RN-xx, assuntos abertos |
| 6 LIs assinadas no modelo antigo (ver abaixo) | LIs reais 2025–2026 | Confirmam a estrutura; trazem gaps reais (gabarito de teste) |
| `San Javier - Integración Facturación Electrónica` (ES, v1.2) | LI real, **saída** do Tasy (Tasy → TIE → PAC), SOAP/XML | Confirma a mesma estrutura da Baxter; mostra telas, parâmetros do Tasy e SQL de apoio dentro do caso de uso; layout das mensagens numa seção separada após os casos de uso |

**Conclusão:** o template oficial é a espinha; as duas LIs reais seguem a **mesma estrutura entre si** (é o padrão de fato das LIs em espanhol) e acrescentam seções úteis. O modelo proposto é o oficial + essas seções, em PT e ES.

### O que as LIs reais têm em comum

- Identificação com cliente, nº do projeto, gerente, processo, consultor e analista do cliente.
- Casos de uso com ID, área, caso de uso e direção, seguidos de regras RN-xx.
- Mapa do processo de negócio antes do detalhamento.
- Por caso de uso: objetivo, ação do usuário no Tasy que dispara, retorno de sucesso e de falha, telas e parâmetros do Tasy.
- Mapeamento com as mesmas colunas: #, campo, documentação/exemplo, obrigatório, tabela, campo Tasy, tipo, tamanho.
- Lista de GAPs com legenda, assuntos abertos, participantes e histórico.
- Nenhuma das duas tem gap registrado ("N/A"): o agente passa a preencher essa seção de fato.

### LIs no modelo antigo (8 LIs, 2025–2026, ES)

`lis-referencia/modelo-antigo/`: Bombas de Infusión (LI02), Pyxis (LI03, 18 casos de uso), Persona Moral (LI06, especificação de ajuste), **Personas Morales MDM (LI10, JSON/API)**, **Registro de Materiales (LI15, JSON/API, SAP → Tasy)**, Diverza Factura y Timbrado, Diverza Auto Facturación (LI16) e MANSIS (LI17).

- **LI10 e LI15 são as LIs via API REST/JSON** que faltavam (endpoints expostos pelo TIE): cobrem pessoa jurídica e cadastro de materiais, as mesmas famílias de APIs que já temos nos Swaggers (`legal_entity`, `material`, `material_group`...).

- **Mesma estrutura** das LIs atuais: confirma o padrão de fato. Diferenças pequenas: "Mapa Mental" (MANSIS), seção 5.2 "Registros y Reglas en el sistema Tasy" (Pyxis) e subfluxos de negócio (Bombas).
- **Layout das mensagens** sempre numa seção própria (7), um subitem por caso de uso, com layout + exemplo — reforça o ponto 5 abaixo.
- **Lista de GAPs preenchida de verdade** em Pyxis e MANSIS (ex.: MANSIS-01 "Crear endpoints para la tabla MAN_EQUIPAMENTO"). São o melhor **gabarito** para testar a classificação do agente.
- **"Especificación de ajuste" (LI06):** é o que hoje se chama **CCI**; usada como referência de CCI.
- **Tamanho:** a Pyxis tem 18 casos de uso; é a referência para testar desempenho e consumo de tokens em LIs grandes.

## Gabarito para testes

Usar as LIs assinadas como casos de teste: o agente recebe só a parte de requisitos e gera a classificação; comparamos com o que a LI real concluiu (APIs/TIE usados e gaps).

| LI | O que testa |
|---|---|
| MANSIS (LI17) | Detecção de gap de API (tabela `MAN_EQUIPAMENTO`); obs.: o índice atual já mostra entidades de API para essa tabela — o gap pode ter sido resolvido depois, o que também testa a versão do Tasy |
| Pyxis (LI03) | Volume (18 CUs), HL7 via TIE, gaps internos |
| Bombas (LI02) | Entrada e saída HL7, dispositivos |
| Diverza / San Javier | Saída SOAP/XML via TIE (faturamento) |
| Personas Morales MDM (LI10) | Entrada JSON; gaps de API em complemento de pessoa jurídica; relevante também para o 4uHub (`pessoa_juridica`) |
| Registro de Materiales (LI15) | Entrada JSON (SAP → Tasy), 9 CUs, gaps de retorno com código gerado no Tasy |

## Lista de tópicos (validada em 19/10/2026)

Legenda — **Auto**: o agente preenche · **Rascunho**: o agente propõe, o consultor valida · **Manual**: só o consultor. Numeração igual à das LIs reais.

| # | Seção | Obrigatória | Preenchimento |
|---|---|---|---|
| — | Identificação (cliente, projeto, GP, consultor, solicitante, classificação, prioridade) | Sim | Manual |
| 1 | Objetivo · 1.1 Formato de comunicação e método · 1.2 Descrição dos sistemas | Sim | Auto / Rascunho |
| 2 | Escopo e responsabilidades | Sim | Rascunho |
| 3 | Descrição geral · 3.1 Objetivo/características · 3.2 Casos de uso · 3.3 Requisitos funcionais (RN-xx) · 3.4 Requisitos não funcionais · 3.5 Premissas · 3.6 Requisitos necessários | Sim | Auto (3.2) / Rascunho |
| 4 | Especificações técnicas — diagrama de arquitetura | Sim | Rascunho |
| 5 | Processos de negócio — mapa | Sim | Rascunho |
| 6 | Procedimentos de integração, **por caso de uso**: objetivo, gatilho no Tasy, telas, passo a passo por sistema, fluxo, casos de teste, especificações técnicas | Sim | Rascunho (telas: Manual) |
| 7 | **Layout e exemplo das mensagens**, um subitem por caso de uso (layout/mapeamento + exemplo) | Sim | Rascunho |
| 8 | Conexão e segurança | Sim | Rascunho |
| 9 | Abreviaturas e definições (9.1 Links adicionais, opcional) | Sim | Auto |
| 10 | Lista de GAPs + legenda | Sim | **Auto** |
| 11 | Assuntos abertos e fechados | Varia por LI | **Auto** |
| 12 | Participantes e aprovadores | Varia por LI | Manual |
| 13 | Histórico de revisão | Sim | Auto |

## O que o agente agrega ao modelo

- **Matriz de viabilidade (interna):** cada caso de uso classificado, com a API ou integração TIE sugerida, a fonte e o nível de confiança — documento separado, só para a equipe.
- **10 Lista de GAPs:** gerada automaticamente a partir dos casos "Gap" e "Parcial", com o objeto do Tasy envolvido.
- **11 Assuntos abertos:** o agente transforma inconsistências do documento e itens de baixa confiança em perguntas ao terceiro (ex.: no 4uHub, o índice que omite o grupo HioAuthorization).
- **6 Mapeamento:** tabela e campo do Tasy vêm dos Swaggers e das entidades das APIs.

## Decisões (Fernando, 19/10/2026)

1. RN-xx (regras de negócio), requisitos não funcionais, mapa do processo, diagrama de arquitetura e abreviaturas são **padrão**; assuntos abertos e aprovadores **variam** por LI.
2. **Idioma:** o plugin pergunta antes de elaborar a LI (PT ou ES).
3. **Template visual:** o `.docx` oficial atual da Bionexo é a base.
4. **Layout das mensagens:** seção própria, **7 – Layout e exemplo das mensagens**.
5. A "Especificación de ajuste" (LI06) é hoje o **CCI** — não é um tipo novo de documento.

6. **Viabilidade não vai para o cliente.** A 3.2 mantém as colunas das LIs reais (ID, área, caso de uso, direção). A análise do agente sai num **anexo interno** separado — *Matriz de viabilidade (uso interno)*, `.xlsx` — com viabilidade, contrato Tasy, fonte e confiança. Os gaps confirmados vão para a seção 10 da LI, como já é feito hoje.

## Diagramas

Gerados por código a partir de um modelo, seguindo o padrão da equipe (BPMN para processos, UML para casos de uso, raias horizontais, esquerda → direita, fim individual por caminho). Saem como imagem no `.docx` e como arquivo editável `.drawio` (mandatório; abre no draw.io e direto no Miro), além de `.bpmn` opcional para Bizagi. Ver [decisão 0012](decisoes/0012-diagramas.md).

## Regra de segurança do agente

Senhas, tokens e chaves que aparecerem no documento do terceiro ou nos exemplos de mensagem são **mascarados** na LI gerada (ex.: `<senha>`).

## Limites conhecidos

- **Tipo e tamanho dos campos** no mapeamento: só disponíveis quando a API documenta no Swagger. Para os demais, o consultor completa.
- **Telas do Tasy e diagramas de arquitetura do cliente** continuam manuais.
