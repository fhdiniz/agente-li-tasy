# Histórico de versões

Formato: `MAIOR.MENOR.CORREÇÃO`.

- **CORREÇÃO** (0.2.**1**): conserto sem mudar o uso (ex.: texto errado no manual, tabela desalinhada).
- **MENOR** (0.**3**.0): novidade compatível (ex.: nova skill, novo tipo de documento, nova seção).
- **MAIOR** (**1**.0.0): mudança que quebra o que já existe (ex.: formato do `conteudo.json` muda) ou a primeira versão oficial para a equipe.

Ao lançar uma versão: atualizar o número nos 4 manifestos (`.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, `gemini-extension.json`, `mcp-server/pyproject.toml`), registrar aqui e criar a tag `vX.Y.Z` no GitHub.

## 0.2.0 — 15/11/2026

Primeira versão utilizável, para testes internos.

- Geração de LI, Manual de Integração e CCI em `.docx` sobre as bases Bionexo Tasy (PT e ES).
- Rascunho automático do manual a partir do catálogo TIE ou do Swagger; rascunho da LI a partir do documento do terceiro.
- Diagramas BPMN, casos de uso e sequência (`.drawio` + `.png`).
- Servidor MCP com 16 ferramentas; skills `gerar-li`, `gerar-manual`, `gerar-cci`, `analisar-viabilidade`, `consultar-tasy`.
- Manifestos para Claude Code, Codex e Gemini CLI (só Claude Code testado).
- Detalhes e limites: `docs/07-reanalise-critica.md`.

## 0.1.0 — 19/10/2026

Concepção: base de conhecimento (índices de Swagger, TIE e PL/SQL), modelos de documento e prova de conceito da classificação de viabilidade.
