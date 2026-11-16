# Agente LI Tasy

Plugin de IA que gera, no padrão Bionexo Tasy:

- **LI** (Levantamento de Integração) a partir do documento de um terceiro, com a matriz interna de viabilidade (**OpenAPI**, **Parcial**, **TIE** ou **Gap**);
- **Manual de Integração** (modelo EMR 12352) a partir do catálogo TIE, de uma API padrão ou de uma LI;
- **CCI** (Control de Cambio de Integración) no formulário oficial.

Meta: uma LI em no máximo 8h. Estado atual, testes e limites: [docs/07-reanalise-critica.md](docs/07-reanalise-critica.md).

## Pré-requisitos

- Uma ferramenta de IA que rode MCP local: **Claude Code**, **Codex** ou **Gemini CLI** (oficiais); Copilot, Cursor e outras (compatíveis).
- [uv](https://docs.astral.sh/uv/) instalado (Windows ou macOS). Não é preciso instalar Python: o uv baixa tudo na primeira execução, que precisa de internet.

## Instalação

| Ferramenta | Como instalar |
|---|---|
| Claude Code | `claude plugin marketplace add <caminho-ou-repo>` e instalar `agente-li`; ou abrir o Claude Code na pasta do repositório |
| Codex | `codex plugin marketplace add <caminho-ou-repo>` e instalar `agente-li` |
| Gemini CLI | `gemini extensions install <caminho-ou-repo>` |
| Outras (Copilot, Cursor...) | Copiar `skills/` e registrar o servidor MCP: comando `uv`, argumentos `run --project <pasta>/mcp-server agente-li` |

Os manifestos do Codex e do Gemini CLI ainda não foram testados nessas ferramentas (ver pendências).

### Instalação manual (Codex, Windows ou macOS)

1. Instale o [uv](https://docs.astral.sh/uv/) (Windows: `winget install astral-sh.uv`) e clone este repositório numa pasta **fora do OneDrive** (ex.: `C:\Projetos\agente-li-tasy`).
2. Prepare uma vez (baixa as bibliotecas): `cd mcp-server` e `uv run pytest -q` (deve mostrar "passed").
3. Registre o servidor em `~/.codex/config.toml` (Windows: `%USERPROFILE%\.codex\config.toml`), com o caminho da sua pasta, usando `/`:

   ```toml
   [mcp_servers.agente-li-tasy]
   command = "uv"
   args = ["run", "--project", "C:/Projetos/agente-li-tasy/mcp-server", "agente-li"]
   startup_timeout_sec = 120
   ```

4. Ligue as skills na pasta do Codex. Windows (PowerShell): `New-Item -ItemType Junction -Path "$HOME\.agents\skills\gerar-manual" -Target "C:\Projetos\agente-li-tasy\skills\gerar-manual"` (repita para cada pasta de `skills/`). macOS: `ln -s <repo>/skills/* ~/.agents/skills/`.
5. No Codex, `/mcp` deve listar `agente-li-tasy`. Para atualizar o plugin depois: `git pull`.

## Uso

> Gere a LI a partir do documento `<arquivo>`.
> Gere o manual da integração `<nome>`.
> Gere o CCI para a mudança `<descrição>`.

O agente pergunta o que faltar (idioma sempre), gera o `.docx` e avisa: **o que está em amarelo no documento cabe análise do consultor**. Detalhes no [guia de uso](docs/04-guia-de-uso.md).

## Estrutura

```
.claude-plugin/  .codex-plugin/  gemini-extension.json  .mcp.json   Manifestos por ferramenta
skills/          Passo a passo que a IA segue (SKILL.md)
mcp-server/      Servidor MCP em Python: base de conhecimento, classificação, diagramas e gerador .docx
templates/       Estrutura das seções (estrutura.json) e bases visuais (.docx) de LI, Manual e CCI
referencias/     Swaggers e índices do Tasy (versionados); referências brutas e documentos de terceiros (só locais)
docs/            Documentação e registro de decisões
saidas/          Documentos gerados (fora do Git)
```

## Desenvolvimento

```
cd mcp-server
uv run pytest                 # testes
uv run agente-li              # servidor MCP (stdio)
uv run python ferramentas/gerar_bases_docx.py ../templates   # regera as bases .docx
```

## Documentação

- [Análise da demanda](docs/01-analise-demanda.md) · [Arquitetura](docs/02-arquitetura.md) · [Pendências](docs/03-pendencias.md)
- [Guia de uso](docs/04-guia-de-uso.md) · [Modelo de LI](docs/05-modelo-li.md) · [Modelos de CCI e Manual](docs/06-modelo-cci-manual.md)
- [Reanálise crítica](docs/07-reanalise-critica.md) · [Registro de decisões](docs/decisoes/)

## Equipe

- Fernando Diniz — responsável e execução
- Angélica — ideação e validação
- Eberton — supervisão
