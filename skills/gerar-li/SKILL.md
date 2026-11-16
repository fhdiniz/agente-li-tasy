---
name: gerar-li
description: Gera a LI (Levantamento de Integração) do Tasy em .docx, no modelo oficial Bionexo Tasy, a partir do documento de um terceiro (PDF, Word, Swagger, planilha, exemplos de mensagem), com a matriz interna de viabilidade (OpenAPI, Parcial, TIE, Gap). Use quando pedirem "gere a LI a partir do documento X", "levantamento de integração" ou "especificação de requisitos da integração".
---

# Gerar LI

O servidor MCP `agente-li-tasy` extrai, consulta a base do Tasy, classifica e gera o documento. Você interpreta, pergunta e redige.

## 1. Perguntar antes de começar (uma única mensagem)

- Documento do terceiro (caminho) e, se for grande, qual parte entra no escopo.
- Idioma da LI: **pt-BR** ou **es** (obrigatório).
- Cliente, nome do projeto, consultor e solicitante (o que não vier fica em amarelo; não invente).
- Classificação: novo processo, alteração ou correção.
- Pasta onde salvar.

## 2. Extrair os pontos de integração

1. Tente `extrair_requisitos` (documentos no padrão "Resumo / Filtros / SQL").
2. Se devolver erro, leia o documento (`ler_documento` em fatias, ou a leitura nativa da sua ferramenta), chame `formatos` e monte o `requisitos.json` você mesmo. SQL do documento passa por `analisar_sql`.
3. Diga ao consultor quantos pontos encontrou, por grupo, e aponte inconsistências do documento (viram assuntos abertos).

Formatos aceitos e não aceitos: `docs/decisoes/0011-formatos-de-entrada.md`. Imagem ou PDF digitalizado: leia por visão e marque tudo como `[[...]]`.

## 3. Classificar a viabilidade

`classificar_viabilidade` grava `classificacao.json` e a matriz interna `.xlsx`.

Confira você mesmo cada linha de confiança **Baixa**: `buscar_apis` (termos em inglês), `detalhar_api`, `consultar_tabela`, `buscar_tie`, `consultar_plsql`. Se concluir outra classe ou outra API, edite `classificacao.json` (`classe`, `api`, `justificativa`) e explique o motivo na justificativa. Se continuar em dúvida, pergunte ao consultor ou deixe como assunto aberto.

A viabilidade **não vai ao cliente**: fica só na matriz interna. Na LI entram os gaps (seção 10).

## 4. Rascunho e redação

1. `rascunho_li` cria o `conteudo.json`: um caso de uso por ponto, tabela 3.2, de-para da seção 7, gaps e assuntos abertos.
2. Chame `formatos` e complete, no idioma da LI:
   - seções 1.2, 2, 3 e 3.1: texto corrido citando os casos de uso na ordem do negócio;
   - regras de negócio (RN-01, RN-02...), requisitos não funcionais e premissas que o documento sustenta;
   - por caso de uso: objetivo, gatilho no Tasy, passo a passo, cenários de teste e especificações técnicas;
   - payloads de exemplo reais do documento, anonimizados;
   - seção 5: mapa do processo em BPMN (bloco `diagrama`); seção 8: conexão e segurança.
3. Junte casos de uso equivalentes (ex.: versões V1.0 e V1.1 do mesmo endpoint) se o consultor concordar.
4. Telas do Tasy, arquitetura do cliente, participantes e aprovadores são do consultor: deixe `[PREENCHER]`.

Regras: nada de senha, token ou credencial; nomes e e-mails só se o consultor informou; o que for inferência fica com `[[...]]`.

## 5. Validar, gerar e responder

`validar_documento`, depois `gerar_documento`. Responda com:

- caminho da LI `.docx`, da matriz interna `.xlsx` ("uso interno, não enviar ao cliente") e dos diagramas `.drawio`;
- resumo: quantos casos de uso por classe e quantos gaps;
- perguntas que só o cliente ou o terceiro respondem;
- "O que está em amarelo no documento cabe análise do consultor."

Depois, ajuste por conversa o que o consultor pedir e gere de novo.
