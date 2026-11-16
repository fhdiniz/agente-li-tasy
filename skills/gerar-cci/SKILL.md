---
name: gerar-cci
description: Gera o CCI (Control de Cambio de Integración / Controle de Mudança de Integração) do Tasy em .docx, no formulário oficial Bionexo Tasy, a partir da descrição da mudança (ata, e-mail, notas) e, se existir, da LI aprovada. Use quando pedirem "gere o CCI", "control de cambio", "controle de mudança da integração" ou "solicitação de mudança".
---

# Gerar CCI

## 1. Perguntar antes de começar (uma única mensagem)

- Descrição da mudança: ata, e-mail ou notas (texto ou caminho do arquivo).
- LI aprovada da integração, se existir (caminho).
- Idioma: **es** ou **pt-BR** (obrigatório).
- Cliente, país, projeto, quem solicitou, data, integração afetada e prioridade do cliente (1 - Alta, 2 - Media, 3 - Baja).
- Pasta onde salvar.

O que o consultor não souber fica em amarelo no formulário. Não invente.

## 2. Analisar a mudança

- Leia a descrição e a LI (`ler_documento`).
- Descubra o que muda no Tasy: `buscar_tie` e `detalhar_tie` (fluxos, rotas e mapeamentos afetados), `buscar_apis`, `detalhar_api`, `consultar_tabela`, `consultar_plsql`.
- Proponha "impactará em": `1 - TIE`, `2 - IBE`, `3 - TIE/IBE` ou `4 - Tasy (Producto)`, e os impactos em testes do fornecedor e no Go Live, sempre com `[[...]]` por ser proposta.

## 3. Montar o conteúdo

Chame `formatos` (item 2) e grave um `conteudo.json` com:

- `campos`: cabeçalho do formulário;
- `solicitacao`: contexto, necessidade do cliente, situação atual e decisões tomadas, com data; registre condicionantes ("não aplicar até a confirmação de X");
- `solucao`: o que a mudança contempla, mais duas tabelas com subtítulo:
  - "Origem da informação no Tasy": cenário, TABELA.CAMPO, tipo/tamanho, atributo JSON ou segmento, destino;
  - "Componentes com impacto previsto": componente (fluxo/mapeamento TIE, API, objeto do Tasy), situação atual, ajuste necessário;
- `regras_negocio`, `comportamento_esperado`, `comportamento_atual` (da LI aprovada, quando houver), `impacto`;
- `informacao_adicional`: evidências da análise e o que falta confirmar com cliente, fornecedor ou equipe técnica.

**Não estime esforço nem custo e não preencha aprovações**: são do consultor.

## 4. Validar, gerar e responder

`validar_documento`, depois `gerar_documento`. Informe o caminho do `.docx`, o que ficou pendente e a frase: "O que está em amarelo no documento cabe análise do consultor."
