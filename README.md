# Agente LI Tasy

Plugin de IA que gera, no padrão Bionexo Tasy:

- **LI** (Levantamento de Integração) a partir do documento de um terceiro, com a matriz interna de viabilidade (**OpenAPI**, **Parcial**, **TIE** ou **Gap**);
- **Manual de Integração** (modelo EMR 12352) a partir do catálogo TIE, de uma API padrão ou de uma LI;
- **CCI** (Control de Cambio de Integración) no formulário oficial.

Meta: uma LI em no máximo 8h. Primeira vez aqui? Vá direto para a [Instalação passo a passo](#instalação-passo-a-passo). Estado atual, testes e limites: [docs/07-reanalise-critica.md](docs/07-reanalise-critica.md).

## Instalação passo a passo

Este guia foi escrito para quem nunca instalou um plugin de IA. Siga as etapas na ordem. Cada comando vem num quadro cinza: copie, cole no terminal e aperte **Enter**.

### Antes de tudo: o que é cada coisa

| Nome | O que é | Precisa instalar? |
|---|---|---|
| **Terminal** | Janela onde se digitam comandos. Windows: **PowerShell** (menu Iniciar, digite "PowerShell"). macOS: **Terminal** (Cmd+Espaço, digite "Terminal") | Não, já vem no computador |
| **Ferramenta de IA** | O programa com que você conversa: Claude Code, Codex ou Gemini CLI | Sim (etapa 3) |
| **Plugin** | Este projeto. Ensina a ferramenta de IA a gerar LI, Manual e CCI | Sim (etapa 4) |
| **uv** | Programa que roda a parte em Python do plugin. Baixa o Python sozinho | Sim (etapa 1) |
| **Git** | Programa que baixa o plugin do GitHub e o atualiza | Sim (etapa 1) |
| **GitHub** | Site onde o plugin fica guardado. O repositório é **privado** | Precisa de conta com acesso (etapa 2) |

### O que a instalação cria sozinha e o que é com você

| Item | Quem cria |
|---|---|
| Pasta do plugin, com skills, servidor, modelos `.docx`, índices e Swaggers do Tasy | **A instalação por link cria sozinha** (dentro da pasta de plugins da ferramenta de IA) |
| Bibliotecas Python e o próprio Python | **O uv baixa sozinho** na primeira vez que o plugin é usado (precisa de internet) |
| Pastas onde saem os documentos gerados (`diagramas/` e outras) | **O plugin cria sozinho** dentro da sua pasta de trabalho |
| uv e Git no computador | **Você** (etapa 1) |
| Acesso ao repositório privado no GitHub | **Você** pede ao responsável (etapa 2) |
| Pasta de trabalho de cada projeto, com o documento do terceiro | **Você** (etapa 5) |
| Pastas `~/.agents/skills` e `~/.codex` | **Você**, só na instalação manual do Codex (está no passo a passo) |

> Não use pasta dentro do **OneDrive** nem para o plugin nem para o trabalho: a sincronização trava arquivos e causa erros.

### Etapa 1. Instalar o uv e o Git

**Windows** (no PowerShell, um comando por vez):

```powershell
winget install --id=astral-sh.uv -e
```

```powershell
winget install --id=Git.Git -e
```

```powershell
winget install --id=GitHub.cli -e
```

**macOS** (no Terminal):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```bash
xcode-select --install
```

O segundo comando instala o Git (abre uma janela: clique em **Instalar**). Para o GitHub CLI, se você usa [Homebrew](https://brew.sh):

```bash
brew install gh
```

Sem Homebrew, baixe o instalador `.pkg` em [cli.github.com](https://cli.github.com).

**Feche o terminal e abra de novo** (senão ele não enxerga os programas novos). Confira:

```bash
uv --version
```

```bash
git --version
```

```bash
gh --version
```

Cada um deve mostrar um número de versão. Se aparecer "não reconhecido" ou "command not found", reinicie o computador e confira de novo.

### Etapa 2. Liberar o acesso ao GitHub

O plugin fica num repositório **privado**. Sem acesso, a instalação falha com "Repository not found" ou pede senha.

1. Crie uma conta em [github.com](https://github.com) (se ainda não tiver).
2. Peça ao responsável pelo projeto (ver [Equipe](#equipe)) para adicionar seu usuário ao repositório `fhdiniz/agente-li-tasy`. Aceite o convite que chega por e-mail.
3. Conecte o computador à sua conta (uma vez só):

   ```bash
   gh auth login
   ```

   Responda: **GitHub.com** → **HTTPS** → **Yes** (autenticar o Git) → **Login with a web browser**. Copie o código de 8 letras que aparece, aperte Enter, cole o código no navegador e autorize.

4. Confira se o acesso funcionou:

   ```bash
   gh repo view fhdiniz/agente-li-tasy
   ```

   Deve mostrar o início deste README. Se der "Could not resolve to a Repository", o convite ainda não foi aceito.

### Etapa 3. Instalar a ferramenta de IA

Escolha **uma**. A recomendada é o **Claude Code**, a única já testada de ponta a ponta com este plugin.

| Ferramenta | Instalação oficial | Comando para abrir |
|---|---|---|
| **Claude Code** (recomendada) | [docs.claude.com/claude-code](https://docs.claude.com/en/docs/claude-code/setup) | `claude` |
| Codex | [developers.openai.com/codex](https://developers.openai.com/codex/cli) | `codex` |
| Gemini CLI | [github.com/google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli) | `gemini` |

Na primeira vez que abrir, a ferramenta pede login com a conta da empresa. Siga o que aparecer na tela.

### Etapa 4. Instalar o plugin

Há dois jeitos. **Use a instalação por link**, que é mais simples e cuida das pastas sozinha. A manual serve para o Codex (cujo link ainda não foi testado), para ferramentas sem suporte a plugin (Cursor, Copilot) ou para quem quer o plugin numa pasta escolhida.

#### 4A. Instalação por link (recomendada)

**Claude Code**: abra o terminal, digite `claude`, aperte Enter e, **dentro do Claude Code**, digite os dois comandos abaixo, um de cada vez:

```text
/plugin marketplace add fhdiniz/agente-li-tasy
```

```text
/plugin install agente-li@bionexo-tasy
```

Quando perguntar o escopo, escolha **user** (vale para todas as pastas). Depois **feche o Claude Code** (digite `/exit`) e abra de novo.

Prefere fazer fora do Claude Code? Os mesmos comandos funcionam direto no terminal:

```bash
claude plugin marketplace add fhdiniz/agente-li-tasy
```

```bash
claude plugin install agente-li@bionexo-tasy
```

**Gemini CLI** (não testado ainda), no terminal:

```bash
gemini extensions install https://github.com/fhdiniz/agente-li-tasy
```

**Codex**: o manifesto existe, mas a instalação por link ainda não foi testada. Use a 4B.

#### 4B. Instalação manual

**Passo 1. Baixe o plugin numa pasta fixa.** Escolha uma pasta que não vai mudar de lugar e **fora do OneDrive**. Os exemplos usam `C:\Projetos` no Windows e `~/Projetos` no macOS (`~` é a sua pasta de usuário).

Windows:

```powershell
New-Item -ItemType Directory -Force C:\Projetos
```

```powershell
git clone https://github.com/fhdiniz/agente-li-tasy C:\Projetos\agente-li-tasy
```

macOS:

```bash
mkdir -p ~/Projetos
```

```bash
git clone https://github.com/fhdiniz/agente-li-tasy ~/Projetos/agente-li-tasy
```

**Passo 2. Prepare o servidor e teste** (baixa o Python e as bibliotecas; demora alguns minutos só na primeira vez).

Windows:

```powershell
uv run --project C:\Projetos\agente-li-tasy\mcp-server pytest -q C:\Projetos\agente-li-tasy\mcp-server
```

macOS:

```bash
uv run --project ~/Projetos/agente-li-tasy/mcp-server pytest -q ~/Projetos/agente-li-tasy/mcp-server
```

No final deve aparecer algo como `12 passed`. Se aparecer `failed`, pare e avise o responsável.

**Passo 3. Ligue o plugin na sua ferramenta.** Siga só a seção da ferramenta que você usa.

<details>
<summary><b>Claude Code (manual)</b></summary>

O Claude Code aceita a pasta local como se fosse o link:

```bash
claude plugin marketplace add C:/Projetos/agente-li-tasy
```

(no macOS: `claude plugin marketplace add ~/Projetos/agente-li-tasy`)

```bash
claude plugin install agente-li@bionexo-tasy
```

</details>

<details>
<summary><b>Codex (manual)</b></summary>

**a) Registre o servidor.** O arquivo de configuração do Codex pode ainda não existir; os comandos abaixo criam a pasta e abrem o arquivo.

Windows:

```powershell
New-Item -ItemType Directory -Force "$HOME\.codex"
```

```powershell
notepad "$HOME\.codex\config.toml"
```

(se o Bloco de Notas perguntar se quer criar o arquivo, clique em **Sim**)

macOS:

```bash
mkdir -p ~/.codex && touch ~/.codex/config.toml && open -e ~/.codex/config.toml
```

Cole no **final** do arquivo, troque o caminho pelo da sua pasta e salve. Use sempre barra normal `/`, mesmo no Windows:

```toml
[mcp_servers.agente-li-tasy]
command = "uv"
args = ["run", "--project", "C:/Projetos/agente-li-tasy/mcp-server", "agente-li"]
startup_timeout_sec = 120
```

No macOS o caminho fica, por exemplo, `"/Users/SEU_USUARIO/Projetos/agente-li-tasy/mcp-server"` (o Codex não entende `~` aqui; descubra o seu com `echo $HOME`).

**b) Ligue as skills.** A pasta de skills pode não existir; o primeiro comando cria. O segundo liga **todas** as skills de uma vez (com atalho, então o `git pull` também as atualiza).

Windows:

```powershell
New-Item -ItemType Directory -Force "$HOME\.agents\skills"
```

```powershell
Get-ChildItem C:\Projetos\agente-li-tasy\skills -Directory | ForEach-Object { New-Item -ItemType Junction -Path "$HOME\.agents\skills\$($_.Name)" -Target $_.FullName }
```

macOS:

```bash
mkdir -p ~/.agents/skills
```

```bash
ln -s ~/Projetos/agente-li-tasy/skills/* ~/.agents/skills/
```

**c) Confira.** Abra o Codex (`codex`) e digite `/mcp`: deve listar `agente-li-tasy`. Digite `$` e veja se aparecem `gerar-li`, `gerar-manual` e `gerar-cci`.

</details>

<details>
<summary><b>Gemini CLI (manual)</b></summary>

```bash
gemini extensions link C:/Projetos/agente-li-tasy
```

(no macOS: `gemini extensions link ~/Projetos/agente-li-tasy`)

</details>

<details>
<summary><b>Cursor, Copilot e outras</b></summary>

Na configuração de servidores MCP da ferramenta, cadastre:

- **nome:** `agente-li-tasy`
- **comando:** `uv`
- **argumentos:** `run`, `--project`, `C:/Projetos/agente-li-tasy/mcp-server`, `agente-li`

Depois aponte a ferramenta para a pasta `skills/` do plugin (ou copie as pastas de dentro dela para onde a ferramenta lê instruções). Cada ferramenta tem a sua tela para isso; procure por "MCP servers" nas configurações.

</details>

### Etapa 5. Primeiro uso e teste

1. Crie uma **pasta de trabalho** para o projeto, por exemplo `C:\Projetos\LI-Hospital-X` (fora do OneDrive), e coloque nela o documento do terceiro. Os documentos gerados saem nessa mesma pasta.
2. Abra o terminal **nessa pasta** e abra a ferramenta de IA:

   ```powershell
   cd C:\Projetos\LI-Hospital-X
   ```

   ```powershell
   claude
   ```

3. Confira se o plugin está ligado: digite `/mcp` e veja `agente-li-tasy` como **connected**.
4. Faça uma pergunta de teste: *"consulte no Tasy qual API grava em AGENDA_CONSULTA"*. Se vier uma lista de APIs, está tudo funcionando.

### Atualizar o plugin

| Instalação | Como atualizar |
|---|---|
| Por link, Claude Code | `/plugin marketplace update bionexo-tasy` dentro do Claude Code e depois reabrir |
| Por link, Gemini CLI | `gemini extensions update agente-li` |
| Manual (qualquer ferramenta) | `git pull` dentro da pasta do plugin (ex.: `cd C:\Projetos\agente-li-tasy` e depois `git pull`) |

A versão instalada e as novidades ficam no [CHANGELOG](CHANGELOG.md).

### Deu problema?

| Sintoma | O que fazer |
|---|---|
| `uv`, `git` ou `gh` "não é reconhecido" / "command not found" | Feche e abra o terminal. Se persistir, reinicie o computador |
| "Repository not found" ou pedido de senha ao instalar | Falta acesso ao repositório privado: refaça a etapa 2 |
| `/mcp` mostra `agente-li-tasy` como **failed** logo após instalar | Na primeira vez o uv baixa o Python e pode passar do tempo limite. Espere 2 minutos, selecione o servidor em `/mcp` e escolha **reconnect** (ou feche e abra a ferramenta) |
| `/mcp` não lista `agente-li-tasy` | O plugin não foi ligado. Claude Code: `/plugin` e veja se `agente-li` está **enabled**. Codex: confira o caminho no `config.toml` |
| Erro de arquivo em uso ou bloqueado | A pasta está no OneDrive: mova para fora |
| Atrás de proxy da empresa e o uv não baixa nada | Peça à TI a liberação de `pypi.org`, `files.pythonhosted.org` e `github.com` |


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
