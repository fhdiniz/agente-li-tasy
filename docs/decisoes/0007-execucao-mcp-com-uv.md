# 0007 — Servidor MCP executado com uv

**Status:** Aceita

## Contexto
O servidor MCP é escrito em Python e roda localmente, na máquina do usuário. Exigir que cada consultor instale e configure o Python e as dependências dificulta a adoção.

## Decisão
Executar o servidor MCP com o [uv](https://docs.astral.sh/uv/). Os manifestos do plugin chamam `uv run` em vez de `python`.

## Premissas

### Python
- O servidor MCP **precisa de Python para rodar**. É ele que executa a extração do documento do terceiro, a indexação dos Swaggers, a classificação de viabilidade e a geração da LI.
- Python foi escolhido por ter as melhores bibliotecas para o que o agente faz: leitura de PDF e DOCX, leitura de OpenAPI (JSON/YAML), análise de SQL e geração de documentos Word. É também a linguagem mais usada para servidores MCP.
- **O usuário não instala nem configura o Python.** O uv fornece uma cópia do Python só para o plugin, separada de qualquer Python que já exista na máquina, sem conflito com outras ferramentas.

### uv
- **O usuário precisa ter o uv instalado na máquina.** É a única instalação além do Claude Code ou do Codex.
- Na primeira execução, o uv baixa a versão correta do Python e as bibliotecas do projeto. Nas seguintes, usa o que já baixou.
- Como as versões ficam travadas no projeto, todos os usuários rodam exatamente o mesmo ambiente, o que torna o resultado reproduzível.

### Em uma frase (para apresentação)
> O plugin roda em Python, mas o usuário não precisa instalar Python: basta instalar o uv, que providencia o Python e as bibliotecas automaticamente na primeira execução.

## Alternativas consideradas
- **Executável único (PyInstaller):** dispensa qualquer instalação, mas exige um build por sistema operacional, e executáveis não assinados costumam ser bloqueados por antivírus corporativo. Fica como plano B caso a TI não permita o uv.
- **Reescrever em Node.js:** apenas troca a dependência do Python pela do Node.

## Sistemas operacionais

**Windows e macOS são obrigatórios** (máquinas dos consultores). O uv tem instalador oficial para os dois. O código do MCP usa só recursos portáveis (caminhos com `pathlib`, sem comandos de shell específicos) e é testado nos dois sistemas a cada versão. A TI confirmou que o uv pode ser instalado (19/10/2026).

## Consequências
- Instalação do usuário: uv + plugin.
- As dependências ficam declaradas em `mcp-server/pyproject.toml`, com versões travadas (`uv.lock`).
- A primeira execução precisa de acesso à internet para baixar Python e dependências.
- Depende de a TI da Philips permitir o uv nas máquinas dos consultores (ver pendências).
