# 0001 — Plugin único para Claude Code e Codex

**Status:** Aceita

## Contexto
A ferramenta de IA corporativa ainda não está definida. Claude Code e Codex compartilham o formato de skills (`SKILL.md`) e suportam servidores MCP.

## Decisão
Um repositório com dois manifestos (`.claude-plugin/` e `.codex-plugin/`), compartilhando skills, servidor MCP e templates.

## Consequências
- O núcleo (MCP + skills) é reaproveitável mesmo se outra ferramenta for adotada.
- É preciso testar o plugin nas duas ferramentas a cada mudança relevante.
