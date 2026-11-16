# 0004 — Documentação em Markdown versionada no Git

**Status:** Aceita

## Contexto
O projeto precisa de registro contínuo de análise, decisões e evolução, e os plugins de Claude Code e Codex são distribuídos a partir de repositórios Git.

## Decisão
Toda a documentação do projeto fica em Markdown, na pasta `docs/` do próprio repositório.

## Consequências
- Documentação versionada junto com o código, com histórico de mudanças.
- Legível no GitHub e pelas próprias ferramentas de IA.
- Documentos de terceiros ficam fora do repositório (`.gitignore`). Material interno da Philips é versionado (ver 0006).
