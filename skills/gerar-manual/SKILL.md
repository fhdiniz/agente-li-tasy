---
name: gerar-manual
description: Gera o Manual de Integração do Tasy (modelo EMR 12352, Bionexo Tasy) em .docx, a partir de uma integração do catálogo TIE, de uma API padrão (Swagger) ou de uma LI aprovada. Use quando pedirem "gere o manual da integração X", "manual de integração", "manual do TIE" ou "manual da API".
---

# Gerar Manual de Integração

O servidor MCP `agente-li-tasy` faz o trabalho pesado. Você conduz a conversa, interpreta e redige.

## 1. Perguntar antes de começar (uma única mensagem)

- Qual integração (nome, cliente ou sistema externo)?
- Idioma do manual: **pt-BR** ou **es**? (obrigatório; nunca presuma)
- Existe LI aprovada, arquivo `.bft` ou outro documento da integração? Peça o caminho.
- Pasta onde salvar o manual.

Se o consultor já informou tudo, não pergunte de novo.

## 2. Localizar a fonte

- Integração via TIE: `buscar_tie` com o nome. Mais de um resultado: mostre a lista e peça para escolher.
- API padrão do Tasy: `buscar_apis`.
- Nada encontrado: diga isso claramente e peça a LI ou a configuração real. Não invente artefatos do TIE.

## 3. Gerar o rascunho

`rascunho_manual` (com `arquivo_bft` ou `api`) grava o `conteudo.json` com as seções do modelo. Conector, evento, fluxo, rota, mapeamento e parâmetros (seção 4.2) já vêm preenchidos do catálogo.

## 4. Completar o conteúdo

Chame `formatos` uma vez e edite o `conteudo.json`:

1. Reescreva no idioma do manual tudo que está com `"revisar": true` (objetivo, características, fluxo, testes). As descrições do catálogo vêm em inglês: traduza e deixe em linguagem de consultor.
2. Use `detalhar_tie`, `detalhar_api`, `consultar_tabela` e `consultar_plsql` para explicar gatilhos, tabelas e APIs. Quanto mais detalhe na seção 4.2, melhor.
3. Se houver LI aprovada, reaproveite: objetivo (seções 1 e 3 da LI), requisitos (3.6), fluxos e casos de teste.
4. Substitua cada `[PREENCHER]` que você consegue responder com evidência. O que depende do cliente (telas, endereços, parâmetros, público) continua como `[PREENCHER: ...]`.
5. Tire o `"revisar"` só do que veio direto da base de conhecimento. Inferência sua fica com `[[...]]`.

Regras: não invente nomes, e-mails, endereços nem parâmetros; nunca escreva senhas ou tokens; dados pessoais trafegados vão na seção 1.3.

## 5. Validar e gerar

`validar_documento` e depois `gerar_documento` (destino `.docx` na pasta combinada). Se houver erro, corrija o JSON e repita.

## 6. Responder ao consultor

- Caminho do `.docx` (e dos diagramas `.drawio`, se houver).
- Lista curta do que ficou pendente para ele preencher.
- A frase final devolvida pela ferramenta: "O que está em amarelo no documento cabe análise do consultor."
- Ofereça ajustar seções por conversa ("detalhe mais o item 4.2.3", "troque o fluxo").
