# Agente LI Tasy

Plugin de IA que gera, no padrão Bionexo Tasy:

- **LI** (Levantamento de Integração) a partir do documento de um terceiro, com a matriz interna de viabilidade (**OpenAPI**, **Parcial**, **TIE** ou **Gap**);
- **Manual de Integração** (modelo EMR 12352) a partir do catálogo TIE, de uma API padrão ou de uma LI;
- **CCI** (Control de Cambio de Integración) no formulário oficial.

Meta: uma LI em no máximo 8h. Primeira vez aqui? Vá direto para a [Instalação passo a passo](#instalação-passo-a-passo). Estado atual, testes e limites: [docs/07-reanalise-critica.md](docs/07-reanalise-critica.md).

## Instalação passo a passo

Este guia foi escrito para quem nunca instalou um plugin de IA. Leia a visão geral, escolha o modo e siga os passos **na ordem**. Cada comando vem num quadro cinza: copie, cole no terminal e aperte **Enter**.

### Visão geral: os dois modos de instalação

O plugin tem duas partes: as **instruções** que a IA segue (pasta `skills/`) e um pequeno **programa em Python** (pasta `mcp-server/`) que consulta a base do Tasy e gera os `.docx`. Há dois jeitos de colocar isso na sua ferramenta de IA:

| | **Modo A: pelo link** (recomendado) | **Modo B: manual** |
|---|---|---|
| **Como funciona** | Você passa o link do plugin para a ferramenta de IA. Ela baixa, instala e cria as pastas sozinha | Você baixa a pasta do plugin para o seu computador e diz à ferramenta de IA onde ela está |
| **Para quem** | **Claude Code** (testado) e Gemini CLI | **Codex**, Cursor, Copilot, ou quem tentou o modo A e não deu certo |
| **Programas necessários** | uv, Git e GitHub CLI | uv. Git e GitHub CLI são opcionais (sem eles, você baixa um ZIP pelo navegador) |
| **Atualizar depois** | Um comando dentro da ferramenta de IA | Um comando (`git pull`) ou baixar o ZIP de novo |

**Na dúvida, use o modo A com o Claude Code.**

#### Por que cada programa?

| Programa | Para que serve, em uma frase | Modo A | Modo B |
|---|---|---|---|
| **Ferramenta de IA** (Claude Code, Codex...) | É com ela que você conversa. O plugin é instalado dentro dela | Sim | Sim |
| **uv** | Roda a parte em Python do plugin. Sem ele, a IA não consegue gerar os documentos | Sim | Sim |
| **Git** | O "link" do plugin é um endereço do GitHub, e o Git é o programa que baixa e atualiza projetos do GitHub. No modo A, a ferramenta de IA usa o Git por baixo dos panos para baixar o plugin. No Windows, o Claude Code também exige o Git para funcionar | Sim | Opcional |
| **GitHub CLI** (`gh`) | O plugin fica num repositório **privado**. O `gh` faz o login do Git na sua conta do GitHub pelo navegador, uma vez só, para ele conseguir baixar | Sim | Opcional |
| **Node.js** | Só é usado para instalar o Codex ou o Gemini CLI | Só se usar Codex ou Gemini | Só se usar Codex ou Gemini |
| **Python** | **Não instale.** O uv baixa uma cópia própria na primeira vez e a mantém separada. Se você já tem Python, não há conflito | Não | Não |

#### Roteiro

1. [Abrir o terminal](#passo-1-abrir-o-terminal)
2. [Verificar o que já está instalado](#passo-2-verificar-o-que-já-está-instalado)
3. [Instalar só o que faltou](#passo-3-instalar-o-que-faltou)
4. [Liberar o acesso ao GitHub](#passo-4-liberar-o-acesso-ao-github)
5. [Instalar o plugin](#passo-5-instalar-o-plugin) (modo A ou modo B)
6. [Testar](#passo-6-testar)

> **Não use pastas dentro do OneDrive**, nem para o plugin nem para o trabalho: a sincronização trava arquivos e causa erros.

### Passo 1. Abrir o terminal

O terminal é a janela onde se digitam comandos. Já vem no computador.

- **Windows: use o PowerShell**, não o "Prompt de Comando" (CMD). Os comandos deste guia foram escritos para o PowerShell e alguns não funcionam no CMD. Para abrir: menu **Iniciar**, digite **PowerShell**, clique em **Windows PowerShell**. Abra normal, **sem** "Executar como administrador". Se abrir o **Terminal** do Windows, tudo bem: ele já usa o PowerShell (a linha começa com `PS C:\...`).
- **macOS: use o Terminal.** Aperte **Cmd + Espaço**, digite **Terminal** e aperte Enter (fica em Aplicativos > Utilitários).

Para colar: no PowerShell, **Ctrl+V** ou **botão direito do mouse**; no Mac, **Cmd+V**. Depois aperte **Enter** e espere a linha de digitação voltar a aparecer.

### Passo 2. Verificar o que já está instalado

Rode cada comando abaixo, **um por vez**, e compare com a tabela.

| Programa | Comando | Se já estiver instalado, aparece | Precisa no modo A | Precisa no modo B |
|---|---|---|---|---|
| uv | `uv --version` | `uv 0.9.5` (ou outro número) | Sim | Sim |
| Git | `git --version` | `git version 2.51.0` (ou outro número) | Sim | Opcional |
| GitHub CLI | `gh --version` | `gh version 2.80.0` (ou outro número) | Sim | Opcional |
| Claude Code | `claude --version` | `2.0.30 (Claude Code)` (ou outro número) | Se for usar o Claude Code | Se for usar o Claude Code |
| Codex | `codex --version` | `codex-cli 0.50.0` (ou outro número) | Se for usar o Codex | Se for usar o Codex |
| Gemini CLI | `gemini --version` | `0.10.0` (ou outro número) | Se for usar o Gemini | Se for usar o Gemini |
| Node.js | `node --version` | `v22.20.0` (ou outro número) | Só para Codex ou Gemini | Só para Codex ou Gemini |

O número exato não importa: **qualquer número de versão significa que está instalado.** Se o programa **não** estiver instalado, aparece um erro como este:

- Windows: `O termo 'uv' não é reconhecido como nome de cmdlet, função, arquivo de script ou programa operável.`
- macOS: `zsh: command not found: uv`

**Anote o que deu erro** e que você precisa no seu modo. Instale só esses itens no passo 3. Se tudo o que você precisa apareceu com número, pule para o [passo 4](#passo-4-liberar-o-acesso-ao-github).

### Passo 3. Instalar o que faltou

Instale **só o que deu erro no passo 2**, nesta ordem. No Windows os comandos usam o **winget**, o instalador oficial da Microsoft que já vem no Windows 10 e 11. Na primeira vez ele pode pedir para aceitar os termos: digite **Y** e aperte Enter.

**Depois de instalar tudo, feche o terminal, abra de novo e repita o passo 2.** O terminal só enxerga programas novos depois de reaberto. Se ainda der erro, reinicie o computador e repita.

#### 3.1 uv

Gerenciador de Python gratuito e de código aberto, da empresa Astral (a mesma do Ruff, muito usado no mercado). Instala só na sua pasta de usuário, não mexe no sistema e não pede administrador. **Liberado pela TI** para as máquinas dos consultores. Site oficial: [docs.astral.sh/uv](https://docs.astral.sh/uv/getting-started/installation/).

Windows (PowerShell):

```powershell
winget install --id=astral-sh.uv -e
```

macOS (Terminal):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### 3.2 Git

Programa padrão, gratuito, para baixar e atualizar projetos do GitHub. Site oficial: [git-scm.com](https://git-scm.com/downloads).

Windows (PowerShell). Se o Windows perguntar "Deseja permitir que este aplicativo faça alterações?", clique em **Sim**:

```powershell
winget install --id=Git.Git -e
```

macOS (Terminal). Abre uma janela: clique em **Instalar** e aceite a licença; demora alguns minutos. Se aparecer "already installed", o Git já está lá:

```bash
xcode-select --install
```

#### 3.3 GitHub CLI

Programa oficial do GitHub para fazer login pelo terminal. Site oficial: [cli.github.com](https://cli.github.com).

Windows (PowerShell):

```powershell
winget install --id=GitHub.cli -e
```

macOS: baixe o instalador em [cli.github.com](https://cli.github.com) (botão **Download for Mac**), abra o arquivo e siga as telas. Quem já usa [Homebrew](https://brew.sh) pode instalar com:

```bash
brew install gh
```

#### 3.4 Node.js (só para Codex ou Gemini CLI)

Plataforma usada para instalar o Codex e o Gemini CLI. **Não é necessária para o Claude Code.** Site oficial: [nodejs.org](https://nodejs.org/pt) (use a versão **LTS**).

Windows (PowerShell):

```powershell
winget install --id=OpenJS.NodeJS.LTS -e
```

macOS: baixe o instalador **LTS** em [nodejs.org](https://nodejs.org/pt), abra e siga as telas.

#### 3.5 Ferramenta de IA

Instale **uma**. A recomendada é o **Claude Code**, a única já testada de ponta a ponta com este plugin. Na primeira vez que abrir, a ferramenta pede login com a conta da empresa: siga o que aparecer na tela.

**Claude Code** ([página oficial](https://docs.claude.com/en/docs/claude-code/setup)). No Windows, instale o Git (3.2) antes.

Windows (PowerShell):

```powershell
irm https://claude.ai/install.ps1 | iex
```

macOS (Terminal):

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Codex** ([página oficial](https://developers.openai.com/codex/cli)). Precisa do Node.js (3.4). Windows e macOS:

```bash
npm install -g @openai/codex
```

**Gemini CLI** ([página oficial](https://github.com/google-gemini/gemini-cli)). Precisa do Node.js (3.4). Windows e macOS:

```bash
npm install -g @google/gemini-cli
```

<details>
<summary>No Windows, o winget não funciona ("winget não é reconhecido")</summary>

Atualize o **Instalador de Aplicativo** pela [Microsoft Store](https://apps.microsoft.com/detail/9nblggh4nns1) e abra o PowerShell de novo. Ou instale cada programa pelo site oficial:

- **uv**: cole no PowerShell o instalador oficial da Astral:

  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```

- **Git**: baixe em [git-scm.com/downloads/win](https://git-scm.com/downloads/win) e clique em **Next** em todas as telas (as opções padrão servem).
- **GitHub CLI**: baixe o instalador `.msi` em [cli.github.com](https://cli.github.com) e clique em **Next** até o fim.
- **Node.js**: baixe a versão **LTS** em [nodejs.org](https://nodejs.org/pt) e clique em **Next** até o fim.

</details>

**Lembrete:** feche o terminal, abra de novo e **repita o passo 2**. Só siga em frente quando tudo o que você precisa aparecer com número de versão.

### Passo 4. Liberar o acesso ao GitHub

O plugin fica num repositório **privado** do GitHub. Sem acesso, a instalação falha com "Repository not found" ou pede senha.

1. Crie uma conta em [github.com](https://github.com), se ainda não tiver.
2. Peça ao responsável pelo projeto (ver [Equipe](#equipe)) para adicionar seu usuário ao repositório `fhdiniz/agente-li-tasy`. **Aceite o convite** que chega por e-mail.
3. **Só para o modo A, ou modo B com Git:** conecte o computador à sua conta (uma vez só):

   ```bash
   gh auth login
   ```

   Responda, usando as setas e Enter: **GitHub.com** → **HTTPS** → **Yes** (autenticar o Git) → **Login with a web browser**. Copie o código de 8 letras que aparece, aperte Enter, cole o código na página que abrir no navegador e autorize.

4. **Confira** se o acesso funcionou:

   ```bash
   gh repo view fhdiniz/agente-li-tasy
   ```

   Deve aparecer o começo deste README. Se aparecer "Could not resolve to a Repository", o convite ainda não foi aceito.

No **modo B com ZIP** basta o item 2: você baixa pelo navegador, já logado no GitHub.

### Passo 5. Instalar o plugin

Siga **só** o modo que você escolheu.

#### Modo A: pelo link

A ferramenta de IA baixa o plugin para a pasta de plugins dela e cria tudo o que precisa. Você não escolhe nem cria pasta nenhuma.

**Claude Code.** No terminal, abra o Claude Code:

```bash
claude
```

Dentro do Claude Code, digite os dois comandos abaixo, um de cada vez:

```text
/plugin marketplace add fhdiniz/agente-li-tasy
```

```text
/plugin install agente-li@bionexo-tasy
```

Se perguntar o escopo da instalação, escolha **user** (vale para todas as pastas). Depois feche o Claude Code com `/exit` e abra de novo.

**Gemini CLI** (ainda não testado), no terminal, fora do Gemini:

```bash
gemini extensions install https://github.com/fhdiniz/agente-li-tasy
```

Pronto. Vá para o [passo 6](#passo-6-testar).

#### Modo B: manual

São três etapas: baixar a pasta do plugin, preparar o servidor e ligar o plugin na ferramenta de IA.

**B1. Baixar a pasta do plugin.** Escolha uma pasta que não vai mudar de lugar, **fora do OneDrive**. Os exemplos usam `C:\Projetos\agente-li-tasy` no Windows e `~/Projetos/agente-li-tasy` no macOS (`~` é a sua pasta de usuário, por exemplo `/Users/maria`).

<details>
<summary><b>Opção 1: com Git</b> (recomendada: atualiza com um comando)</summary>

Windows (PowerShell):

```powershell
New-Item -ItemType Directory -Force C:\Projetos
```

```powershell
git clone https://github.com/fhdiniz/agente-li-tasy C:\Projetos\agente-li-tasy
```

macOS (Terminal):

```bash
mkdir -p ~/Projetos
```

```bash
git clone https://github.com/fhdiniz/agente-li-tasy ~/Projetos/agente-li-tasy
```

</details>

<details>
<summary><b>Opção 2: sem Git, baixando um ZIP</b></summary>

1. Entre no GitHub pelo navegador, já logado, e abra [github.com/fhdiniz/agente-li-tasy](https://github.com/fhdiniz/agente-li-tasy).
2. Clique no botão verde **Code** e depois em **Download ZIP**.
3. Crie a pasta `C:\Projetos` (Windows) ou `Projetos` dentro da sua pasta de usuário (macOS).
4. Extraia o ZIP dentro dela. Windows: botão direito no arquivo > **Extrair tudo**. macOS: dois cliques no arquivo.
5. A pasta extraída se chama `agente-li-tasy-main`. **Renomeie para `agente-li-tasy`.**
6. **Confira:** abrindo `agente-li-tasy`, você deve ver logo de cara as pastas `mcp-server`, `skills` e `templates`. Se aparecer outra pasta `agente-li-tasy-main` dentro, use essa de dentro no lugar.

</details>

**B2. Preparar o servidor e conferir.** Este comando baixa o Python e as bibliotecas (alguns minutos, só na primeira vez) e roda os testes do plugin.

Windows (PowerShell):

```powershell
uv run --project C:\Projetos\agente-li-tasy\mcp-server pytest -q C:\Projetos\agente-li-tasy\mcp-server
```

macOS (Terminal):

```bash
uv run --project ~/Projetos/agente-li-tasy/mcp-server pytest -q ~/Projetos/agente-li-tasy/mcp-server
```

No final deve aparecer algo como `12 passed`. Se aparecer `failed` ou `error`, pare e avise o responsável.

**B3. Ligar o plugin na ferramenta de IA.** Abra só a da sua ferramenta.

<details>
<summary><b>Claude Code</b></summary>

No terminal (fora do Claude Code), use o caminho da pasta no lugar do link:

Windows:

```powershell
claude plugin marketplace add C:/Projetos/agente-li-tasy
```

macOS:

```bash
claude plugin marketplace add ~/Projetos/agente-li-tasy
```

Depois, nos dois sistemas:

```bash
claude plugin install agente-li@bionexo-tasy
```

</details>

<details>
<summary><b>Codex</b></summary>

O Codex precisa de duas coisas: saber onde está o servidor (arquivo `config.toml`) e enxergar as skills (pasta `.agents/skills`). Essas pastas podem não existir ainda; os comandos abaixo as criam.

**a) Registrar o servidor.**

Windows (PowerShell), um comando de cada vez:

```powershell
New-Item -ItemType Directory -Force "$HOME\.codex"
```

```powershell
notepad "$HOME\.codex\config.toml"
```

Se o Bloco de Notas perguntar se quer criar o arquivo, clique em **Sim**.

macOS (Terminal):

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

No macOS o caminho fica, por exemplo, `"/Users/maria/Projetos/agente-li-tasy/mcp-server"`. O Codex não entende `~` aqui; para descobrir o começo do seu caminho, rode `echo $HOME`.

**b) Ligar as skills.** O primeiro comando cria a pasta; o segundo liga todas as skills de uma vez, por atalho (assim, quando o plugin for atualizado, as skills também são).

Windows (PowerShell):

```powershell
New-Item -ItemType Directory -Force "$HOME\.agents\skills"
```

```powershell
Get-ChildItem C:\Projetos\agente-li-tasy\skills -Directory | ForEach-Object { New-Item -ItemType Junction -Path "$HOME\.agents\skills\$($_.Name)" -Target $_.FullName }
```

macOS (Terminal):

```bash
mkdir -p ~/.agents/skills
```

```bash
ln -s ~/Projetos/agente-li-tasy/skills/* ~/.agents/skills/
```

**c) Conferir.** Abra o Codex (`codex`) e digite `/mcp`: deve listar `agente-li-tasy`. Digite `$` e veja se aparecem `gerar-li`, `gerar-manual` e `gerar-cci`.

</details>

<details>
<summary><b>Gemini CLI</b></summary>

Windows:

```powershell
gemini extensions link C:/Projetos/agente-li-tasy
```

macOS:

```bash
gemini extensions link ~/Projetos/agente-li-tasy
```

</details>

<details>
<summary><b>Cursor, Copilot e outras</b></summary>

Na tela de configuração de servidores MCP da ferramenta (procure por "MCP servers" nas configurações), cadastre:

- **nome:** `agente-li-tasy`
- **comando:** `uv`
- **argumentos:** `run`, `--project`, `C:/Projetos/agente-li-tasy/mcp-server`, `agente-li`

Depois aponte a ferramenta para a pasta `skills/` do plugin, ou copie as pastas de dentro dela para onde a ferramenta lê instruções.

</details>

### Passo 6. Testar

1. Crie uma **pasta de trabalho** para o projeto, por exemplo `C:\Projetos\LI-Hospital-X` (fora do OneDrive), e coloque nela o documento do terceiro. Os documentos gerados saem nessa mesma pasta; as subpastas (como `diagramas/`) o plugin cria sozinho.
2. No terminal, entre nessa pasta e abra a ferramenta de IA (exemplo com o Claude Code no Windows):

   ```powershell
   cd C:\Projetos\LI-Hospital-X
   ```

   ```powershell
   claude
   ```

3. Digite `/mcp`. Deve aparecer `agente-li-tasy` como **connected**. Na primeira vez pode demorar até 2 minutos, porque o uv baixa o Python.
4. Faça uma pergunta de teste: *"consulte no Tasy qual API grava em AGENDA_CONSULTA"*. Se vier uma lista de APIs, **está tudo funcionando**.

### Atualizar o plugin

| Como instalou | Como atualizar |
|---|---|
| Modo A, Claude Code | Dentro do Claude Code: `/plugin marketplace update bionexo-tasy`, depois feche e abra de novo |
| Modo A, Gemini CLI | No terminal: `gemini extensions update agente-li` |
| Modo B com Git | No terminal: `git -C C:\Projetos\agente-li-tasy pull` (macOS: `git -C ~/Projetos/agente-li-tasy pull`) |
| Modo B com ZIP | Baixe o ZIP de novo, apague a pasta `agente-li-tasy` antiga e repita a opção 2 do B1 (o B3 não precisa repetir) |

A versão instalada e as novidades ficam no [CHANGELOG](CHANGELOG.md).

### Deu problema?

| Sintoma | O que fazer |
|---|---|
| "não é reconhecido" ou "command not found" logo depois de instalar | Feche e abra o terminal. Se persistir, reinicie o computador |
| "Repository not found" ou pedido de senha ao instalar | Falta acesso ao repositório privado: refaça o [passo 4](#passo-4-liberar-o-acesso-ao-github) |
| `/mcp` mostra `agente-li-tasy` como **failed** logo após instalar | Na primeira vez o uv baixa o Python e pode passar do tempo limite. Espere 2 minutos, selecione o servidor em `/mcp` e escolha **reconnect** (ou feche e abra a ferramenta) |
| `/mcp` não lista `agente-li-tasy` | O plugin não foi ligado. Claude Code: digite `/plugin` e veja se `agente-li` está **enabled**. Codex: confira o caminho no `config.toml` |
| Erro de arquivo em uso ou bloqueado | A pasta está no OneDrive: mova para fora |
| Rede da empresa bloqueia downloads | Peça à TI para liberar `github.com`, `pypi.org` e `files.pythonhosted.org` |


## Comandos do plugin

Você pode chamar cada função pelo atalho da sua ferramenta ou simplesmente escrevendo a frase, em português, no chat. As duas formas dão o mesmo resultado.

| O que faz | Claude Code | Codex | Gemini, Cursor, Copilot | Exemplo de frase |
|---|---|---|---|---|
| **Gerar a LI** completa a partir do documento do terceiro, com a matriz interna de viabilidade | `/agente-li:gerar-li` | `$gerar-li` | Frase | *Gere a LI a partir do documento `Evya-4uHub.pdf`* |
| **Gerar o Manual de Integração** (modelo EMR 12352) a partir de uma integração TIE, de uma API padrão ou de uma LI aprovada | `/agente-li:gerar-manual` | `$gerar-manual` | Frase | *Gere o manual da integração URA Avaya* |
| **Gerar o CCI** (controle de mudança) no formulário oficial | `/agente-li:gerar-cci` | `$gerar-cci` | Frase | *Gere o CCI para a mudança: desativar a rota do código de devedor* |
| **Só analisar a viabilidade** (OpenAPI, Parcial, TIE ou Gap), sem gerar a LI | `/agente-li:analisar-viabilidade` | `$analisar-viabilidade` | Frase | *Analise a viabilidade do documento `Evya-4uHub.pdf`* |
| **Consultar a base do Tasy** (APIs, tabelas, integrações TIE, PL/SQL) | `/agente-li:consultar-tasy` | `$consultar-tasy` | Frase | *Consulte no Tasy qual API grava em AGENDA_CONSULTA* |

O agente sempre pergunta o idioma (português ou espanhol) e o que mais faltar antes de gerar. Ao terminar, avisa: **o que está em amarelo no documento cabe análise do consultor**. Mais detalhes no [guia de uso](docs/04-guia-de-uso.md).

<details>
<summary>Ferramentas internas (a IA usa sozinha; você não precisa chamar)</summary>

Os comandos acima usam estas ferramentas do servidor MCP. Elas aparecem na tela quando a IA pede permissão para usá-las.

| Ferramenta | O que faz |
|---|---|
| `ler_documento` | Lê o texto de PDF, Word, Markdown ou TXT quando a IA não consegue abrir o arquivo sozinha |
| `extrair_requisitos` | Extrai os pontos de integração de documentos no padrão "Resumo / Filtros / SQL" (ex.: Evya) |
| `analisar_sql` | Lista tabelas, colunas e procedures do Tasy citadas num SQL do terceiro |
| `classificar_viabilidade` | Classifica cada ponto (OpenAPI, Parcial, TIE ou Gap) e gera a matriz interna `.xlsx` |
| `buscar_apis` / `detalhar_api` | Procura APIs padrão do Tasy e mostra os campos com tabela e coluna |
| `consultar_tabela` | Mostra tudo que existe no Tasy para uma tabela: APIs, PL/SQL, eventos e integrações TIE |
| `consultar_plsql` | Mostra assinatura, tabelas gravadas e eventos de procedures e functions do Tasy |
| `buscar_tie` / `detalhar_tie` | Procura integrações no catálogo TIE e mostra eventos, fluxos e mapeamentos |
| `rascunho_li` / `rascunho_manual` | Monta o primeiro rascunho da LI ou do Manual para a IA revisar |
| `validar_documento` | Confere se o conteúdo tem todas as seções obrigatórias do modelo oficial |
| `gerar_documento` | Gera o `.docx` final (LI, Manual ou CCI) no visual Bionexo Tasy |
| `gerar_diagrama` | Desenha BPMN, casos de uso e sequência (`.drawio` editável e `.png`) |
| `formatos` | Guia interno dos formatos de arquivo que a IA usa |

</details>

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
