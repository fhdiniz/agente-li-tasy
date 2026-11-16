# Contexto para agentes de IA

Este arquivo dá contexto a qualquer ferramenta de IA que trabalhe neste repositório (Codex, Claude Code e outras que leem AGENTS.md).

## Projeto
Plugin que gera, no padrão Bionexo Tasy, a **LI (Levantamento de Integração)**, o **Manual de Integração** e o **CCI (controle de mudança)** do Tasy. Cruza o documento do terceiro com as APIs OpenAPI do Tasy (Swagger), o catálogo TIE e o PL/SQL, e classifica a viabilidade de cada ponto: **OpenAPI**, **Parcial**, **TIE** ou **Gap**.

Meta: LI concluída em no máximo 8h.

## Onde está cada coisa
- `mcp-server/agente_li/`: servidor MCP e núcleo (índices, extração, classificação, rascunhos, diagramas, gerador `.docx`). Testes: `cd mcp-server && uv run pytest`.
- `skills/`: `gerar-li`, `gerar-manual`, `gerar-cci`, `analisar-viabilidade`, `consultar-tasy`.
- `templates/<li|manual|cci>/`: `estrutura.json` (seções) e `base-<idioma>.docx` (visual). As bases são geradas por `mcp-server/ferramentas/gerar_bases_docx.py`: não editar à mão.
- `.claude-plugin/`, `.codex-plugin/`, `gemini-extension.json`, `.mcp.json`: manifestos.

## Base de conhecimento
- `referencias/openapi/`: Swaggers das APIs do Tasy.
- `referencias/indices/`: índices extraídos do código do Tasy e do catálogo TIE. Comece por `referencias/indices/tabelas.json` e leia o [README](referencias/indices/README.md) antes de usar.

## Leia antes de começar
1. `docs/01-analise-demanda.md` — a demanda e a análise do documento da Evya (Portal 4uHub)
2. `docs/02-arquitetura.md` — arquitetura do plugin
3. `docs/decisoes/` — decisões tomadas e por quê
4. `docs/03-pendencias.md` — o que está em aberto
5. `docs/04-guia-de-uso.md` — como o usuário final usa o plugin
6. `docs/05-modelo-li.md` e `templates/li/estrutura.json` — o modelo de LI que o agente preenche
7. `docs/06-modelo-cci-manual.md` e `templates/{cci,manual}/` — CCI e Manual
8. `docs/07-reanalise-critica.md` — estado atual, testes feitos e limites conhecidos

## Regras do repositório
- Lógica determinística (extração, indexação, classificação, rascunho, geração) fica em código no `mcp-server/`, não em prompt. A IA redige e confere (decisão 0014).
- Mudou código do `mcp-server/`? Rode os testes e gere de novo um documento de cada tipo.
- `referencias/openapi`, `tie` e `lis-referencia` são material interno da Philips, versionado em repositório privado: não publicar fora dele.
- `referencias/documentos-terceiros/` é confidencial do terceiro: **nunca** versionar nem copiar para arquivos versionados.
- Toda decisão relevante vira um novo arquivo em `docs/decisoes/`.
- Atualize `docs/03-pendencias.md` ao concluir ou criar pendências.
- Nova versão do plugin: mesmo número nos 4 manifestos e entrada no `CHANGELOG.md` (o teste `test_versao_igual_nos_manifestos` confere).
- Documentação em português, em Markdown.
- Skills seguem só o padrão Agent Skills (`SKILL.md`), sem extensões específicas de uma ferramenta (decisão 0009).
- Referências em `modelo-antigo/` servem só para conteúdo; estrutura e visual vêm sempre de `templates/`.
- Documentos gerados: só incerteza e pendência saem com realce amarelo (decisões 0010 e 0014). Nunca senhas ou tokens. Formatos de entrada aceitos: decisão 0011.
- Nunca leia inteiros os arquivos de `referencias/indices/` nem os Swaggers: consulte pelo servidor MCP ou com busca filtrada.
