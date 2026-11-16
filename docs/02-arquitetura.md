# Arquitetura

## Visão geral

Um único repositório com um manifesto por ferramenta (Claude Code, Codex e Gemini CLI) que compartilham as mesmas skills e o mesmo servidor MCP. Todas usam o formato `SKILL.md` (especificação Agent Skills) e servidores MCP.

| Camada | Conteúdo | Compartilhado |
|---|---|---|
| Servidor MCP (Python) | Extração do documento do terceiro, índice OpenAPI, busca TIE, classificação de viabilidade, geração da LI | Sim |
| Skills | `gerar-li`, `gerar-manual`, `gerar-cci`, `analisar-viabilidade`, `consultar-tasy` (ver [guia de uso](04-guia-de-uso.md) e [06-modelo-cci-manual](06-modelo-cci-manual.md)) | Sim |
| Templates | Estrutura de conteúdo + template visual da LI | Sim |
| Manifestos | `.claude-plugin/`, `.codex-plugin/`, `gemini-extension.json` e `.mcp.json` | Um por ferramenta |

## Premissas de uso

- Plugin construído só com padrões abertos (Agent Skills, MCP, `AGENTS.md`): suporte oficial a Claude Code e Codex, compatível com outras ferramentas ([decisão 0009](decisoes/0009-padrao-multiplataforma.md)).

- O usuário usa **Claude Code** ou **Codex**. O ChatGPT (chat) exigiria o servidor MCP hospedado na nuvem e não está no escopo atual (ver [MCP local x MCP na nuvem](#mcp-local-x-mcp-na-nuvem)).
- O servidor MCP é escrito em **Python** e precisa dele para rodar, mas o usuário **não instala Python**: o **uv** (único pré-requisito) fornece o Python e as bibliotecas na primeira execução, isolados do restante da máquina ([decisão 0007](decisoes/0007-execucao-mcp-com-uv.md)).
- A primeira execução tem acesso à internet.

## MCP local x MCP na nuvem

O servidor MCP é o "motor" do plugin: o programa que faz o trabalho pesado (extração, cruzamento, classificação e geração da LI). Ele pode rodar em dois lugares:

| | MCP local (escolhido) | MCP na nuvem |
|---|---|---|
| Onde roda | Na máquina do usuário | Em um servidor, acessado pela internet (HTTPS) |
| Ferramentas | Claude Code e Codex | Necessário para o ChatGPT (chat); também serve Claude e Codex |
| Material de referência | Lido da pasta do plugin, na própria máquina | Fica no servidor |
| Documento do terceiro | Não sai da máquina do usuário | Precisa ser enviado ao servidor |
| Infraestrutura | Nenhuma; cada usuário instala o uv | Servidor, autenticação, segurança e manutenção pela TI |
| Pré-requisito do usuário | uv instalado | Nenhum além do acesso |

**Por que local agora:** começa sem depender de infraestrutura nem de aprovação da TI, e o material interno e os documentos de terceiros não saem da máquina do usuário.

**Se no futuro o ChatGPT (chat) for adotado:** o ChatGPT só aceita MCP remoto, então o mesmo servidor precisará ser hospedado em ambiente da Philips, com autenticação. O código Python é o mesmo; muda onde ele roda e como o documento do terceiro entra e o .docx gerado volta ao usuário. Situação levantada em outubro de 2026: plugins do ChatGPT aceitam MCP remoto, com uso completo em beta nos planos Business/Enterprise/Edu e dependente de liberação do administrador.

## Princípio central

**Lógica em código, não em prompt.** Extração, indexação, classificação, rascunho e geração são determinísticas no MCP, para que o resultado seja reproduzível e auditável. O modelo interpreta, redige, confere as conclusões de baixa confiança e trata os casos ambíguos ([decisão 0014](decisoes/0014-rascunho-em-codigo-ia-revisa.md)).

## Fluxo

1. Ingestão do documento do terceiro.
2. Extração estruturada: endpoint, método, campos, tabelas, operação.
3. Cruzamento com o índice OpenAPI e o catálogo TIE.
4. Classificação de viabilidade com nível de confiança.
5. Rascunho do conteúdo em JSON (código) e redação pela IA.
6. Validação contra a estrutura oficial e geração do `.docx` e dos diagramas.
7. Revisão humana do que está em amarelo.

Manual e CCI seguem os passos 5 a 7, partindo do catálogo TIE, do Swagger ou da descrição da mudança.

## Módulos do servidor MCP (`mcp-server/agente_li/`)

| Módulo | Função |
|---|---|
| `indices.py`, `openapi_idx.py` | Consultas à base de conhecimento (APIs, tabelas, PL/SQL, TIE) |
| `terceiro.py` | Leitura de PDF e extração dos pontos de integração; análise de SQL |
| `classificar.py`, `matriz.py` | Viabilidade com evidências e matriz interna `.xlsx` |
| `rascunhos.py` | Rascunho de LI, Manual de integração TIE e Manual de API |
| `diagrama.py` | BPMN, casos de uso e sequência: valida e gera `.drawio` + `.png` |
| `documento.py` | Valida o conteúdo e gera o `.docx` sobre a base; mascara segredos |
| `servidor.py` | As 16 ferramentas MCP; `formato.md` documenta os formatos para a IA |

## Base de conhecimento

Além dos Swaggers, o agente consulta índices extraídos do código-fonte do Tasy e do catálogo TIE (`referencias/indices/`): para cada tabela, quais APIs a gravam, quais integrações TIE a usam e quais objetos PL/SQL a alteram. Ver [decisão 0008](decisoes/0008-codigo-fonte-indexar-nao-versionar.md).

## Índice OpenAPI

Os arquivos Swagger ficam separados, um por API. O MCP lê a pasta inteira na inicialização e monta um índice por operação (API, método, path, campos de entrada e saída, tipos, descrições). O agente consulta o índice, sem carregar os Swaggers inteiros.

## Template da LI

Duas camadas:

1. **Estrutura de conteúdo** (YAML/JSON): seções, obrigatoriedade e o que cada seção espera. É o que o agente preenche.
2. **Template visual** (.docx): layout e estilos. Geração determinística.

Novos tipos de documento (Manual de Operação, aderência) passam a ser uma nova estrutura de conteúdo com um novo template, sem alterar o motor.
