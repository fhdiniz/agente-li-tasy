# 0013 — Documento mestre por tipo de documento; referências brutas fora do Git

**Status:** Aceita (19/10/2026), condicionada ao inventário de cobertura abaixo

## Contexto
As LIs, CCIs e manuais de referência têm nomes, e-mails e assinaturas de clientes. Versioná-los exige anonimizar dezenas de arquivos. Além disso, ler 10+ PDFs a cada execução custa tempo e tokens.

## Decisão
Cada tipo de documento (LI, CCI, Manual) tem um **documento mestre** versionado, que concentra tudo o que o agente precisa — sem dados de clientes:

| Arquivo | Conteúdo |
|---|---|
| `templates/<tipo>/estrutura.json` | Seções, numeração, obrigatoriedade, colunas das tabelas, valores permitidos, instruções e quem preenche |
| `templates/<tipo>/perfil.json` | Formatação extraída do `.docx` oficial: página, margens, fontes, tamanhos, cores, espaçamentos, estilos de título, cabeçalho/rodapé, sumário, listas suspensas |
| `templates/<tipo>/*.docx` | Template oficial **limpo** (sem dados de clientes) — o gerador parte dele, herdando estilos, capa e rodapé |
| `docs/05` e `docs/06` | Padrões observados nas referências reais e decisões do grupo |

As referências brutas (`referencias/lis-referencia/`, `cci-referencia/`, `manuais-referencia/`) ficam **só na máquina local**, fora do Git. O gabarito de testes (casos de uso e conclusões das LIs assinadas) será extraído para um arquivo próprio, sem nomes de pessoas.

## Bases `.docx` (uma por tipo e idioma)

O gerador herda estilo, capa, cabeçalho e rodapé de um `.docx` base limpo. Como o idioma é perguntado antes de gerar, cada tipo precisa de uma base em cada idioma:

| Tipo | Português | Espanhol | Origem |
|---|---|---|---|
| LI | `templates/li/base-pt-BR.docx` | `templates/li/base-es.docx` (derivada) | Template oficial PT |
| CCI | `templates/cci/base-pt-BR.docx` (derivada) | `templates/cci/base-es.docx` | Template CCI ES, exemplo removido |
| Manual | `templates/manual/base-pt-BR.docx` (derivada) | `templates/manual/base-es.docx` | EMR 12352 ES |

Geradas por `mcp-server/ferramentas/gerar_bases_docx.py`:
- **LI e Manual:** capa, cabeçalho, rodapé, sumário (campo vazio, o Word refaz ao abrir) e tabela de identificação; o corpo é montado pelo gerador a partir de `estrutura.json`.
- **CCI:** o formulário inteiro, com as listas suspensas; valores do exemplo trocados por marcadores (`<Cliente>`, `<DD/MMM/AAAA>`) e textos por instruções (`[Descrever ...]`).
- Textos fixos traduzidos; autor do arquivo trocado por "Bionexo Tasy".
- O rótulo "Gerente de projetos de implantação **Philips**" do template oficial passou a "**Bionexo Tasy**" nas duas bases da LI.

Os templates oficiais originais continuam em `templates/` como referência.

## Garantia de não perder nada

1. **As referências brutas não são apagadas**: continuam na pasta local do responsável (com backup no OneDrive). Só deixam de ser distribuídas com o plugin.
2. **Inventário de cobertura** (`templates/cobertura.md`): para cada referência real, lista seções, tabelas e colunas, valores de listas, regras e estilos encontrados, e onde cada item está no mestre (`estrutura.json`, `perfil.json`, `docs/05`, `docs/06`). Item sem destino = lacuna a corrigir antes de aceitar a referência como coberta.
3. **Gabarito de testes** (`testes/gabarito.json`): casos de uso, contratos Tasy usados e gaps das LIs assinadas, **sem nomes de pessoas** — preserva o conhecimento técnico das referências.
4. Nova referência recebida → rodar de novo a análise e atualizar o mestre e o inventário.

## Consequências
- Repositório sem dados pessoais de clientes; nada a anonimizar nas referências brutas.
- O agente lê arquivos pequenos e estruturados em vez de PDFs → mais rápido e mais barato.
- O `.docx` oficial continua necessário: o perfil documenta a formatação, mas o gerador **herda** os estilos do template em vez de recriá-los (mais fiel).
- Para atualizar o mestre com novas referências, rodar de novo a análise localmente.
