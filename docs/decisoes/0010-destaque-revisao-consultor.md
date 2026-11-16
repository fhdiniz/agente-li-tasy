# 0010 — Destaque do que cabe ao consultor revisar

**Status:** Aceita

## Contexto
O documento gerado mistura conteúdo confiável (extraído das fontes) com conteúdo que exige análise humana: dados pessoais, campos que só o consultor sabe, conclusões de baixa confiança. O consultor precisa achar esses pontos rápido, e eles não podem passar despercebidos para o cliente.

## Decisão
Tudo o que cabe ao consultor analisar ou preencher sai com **realce amarelo** no `.docx` (marca-texto do Word):

| O que | Como aparece |
|---|---|
| Campo a preencher (não há dado) | `[PREENCHER: <o que é>]` com realce amarelo |
| Dado a confirmar (nomes, e-mails, cargos, datas, versões, valores sugeridos) | Texto sugerido com realce amarelo |
| Conclusão de confiança média/baixa (ex.: viabilidade "Parcial") | Texto com realce amarelo + nota "confirmar" |

Ao terminar, a resposta do agente traz o aviso **"O que está em amarelo no documento cabe análise do consultor"**, com a quantidade de itens e a lista por seção.

Por que amarelo e não texto vermelho: realce é encontrado na hora, não se confunde com erro, mantém a cor original do modelo e é removido em um clique depois da revisão.

## Consequências
- Seções `manual` saem como `[PREENCHER]`. Nas seções `rascunho`, só a incerteza vai em amarelo (ver [decisão 0014](0014-rascunho-em-codigo-ia-revisa.md)); texto vindo do terceiro ou da base de conhecimento não.
- Antes de enviar ao cliente, o documento não pode ter realce amarelo (o agente avisa se ainda houver).
