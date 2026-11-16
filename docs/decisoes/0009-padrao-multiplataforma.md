# 0009 — Padrão único para qualquer ferramenta de IA

**Status:** Aceita (amplia a [0001](0001-plugin-unico-claude-codex.md))

## Contexto
A ferramenta de IA corporativa ainda não está definida e pode variar entre equipes. As principais ferramentas de IA para desenvolvimento adotaram três padrões abertos: **Agent Skills** (`SKILL.md`, especificação em agentskills.io, adotada por Claude Code, Codex, Gemini CLI, Cursor, Kiro e 30+ ferramentas), **MCP** e **`AGENTS.md`**.

## Decisão
O plugin usa apenas esses três padrões, com quatro regras:

1. **Skills só no formato padrão** do `SKILL.md`: frontmatter padrão, `name` igual ao nome da pasta, menos de 500 linhas, detalhes em `references/`. Nenhuma extensão específica de uma ferramenta.
2. **Toda lógica no servidor MCP.** A skill orienta o passo a passo; extração, consulta e classificação ficam no MCP. Qualquer ferramenta que fale MCP obtém o mesmo resultado.
3. **Mesmo nome de skill e mesma frase de uso em todas as ferramentas.** O atalho muda por ferramenta, mas o pedido em linguagem natural ("gere a LI a partir do documento X") funciona em todas.
4. **Dois níveis de suporte:**

| Nível | Ferramentas | Instalação | Garantia |
|---|---|---|---|
| Oficial | Claude Code, Codex, **Gemini CLI** (Google) | Plugin/extensão: `.claude-plugin/`, `.codex-plugin/` e `gemini-extension.json` (as extensões do Gemini CLI aceitam skills `SKILL.md` e servidor MCP local) | Testado a cada versão |
| Compatível | Cursor, Copilot e outras com Agent Skills + MCP local | Manual: copiar `skills/` e configurar o MCP | Deve funcionar, sem teste garantido |
| Não suportado hoje | ChatGPT (chat), Manus | — | Rodam na nuvem e não alcançam o MCP local nem a base de conhecimento da máquina; exigiriam o MCP hospedado (ver `02-arquitetura`, "MCP local x MCP na nuvem") |

Definido (Fernando, 19/10/2026): **oficiais** Claude Code, Codex e Gemini CLI; **compatíveis** as demais que rodam MCP local.

## Consequências
- Troca de ferramenta não exige reescrever o plugin.
- A qualidade do resultado ainda depende do modelo de cada ferramenta; por isso só o nível oficial é testado.
- Validar as skills contra a especificação (ex.: `skills-ref validate`) antes de cada versão.
