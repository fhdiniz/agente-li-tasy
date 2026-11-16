# 0014 — Rascunho em código, IA redige e confere, amarelo só para incerteza

**Status:** Aceita (ajusta a [0010](0010-destaque-revisao-consultor.md) e detalha o princípio "lógica em código")

## Contexto
A reanálise de novembro de 2026 mostrou três problemas: a classificação automática era tratada como resposta final sem nunca ter sido conferida; pedir à IA o documento inteiro gasta tokens e varia entre execuções; e marcar em amarelo toda seção "rascunho" deixaria o documento quase todo amarelo.

## Decisão
1. **O código faz o rascunho.** `rascunho_li` e `rascunho_manual` montam um `conteudo.json` com tudo o que a base de conhecimento responde: casos de uso, de-para de campos, conector, evento, fluxo, rota, gaps.
2. **A IA redige e confere.** Ela reescreve os trechos narrativos, traduz, responde os `[PREENCHER]` que têm evidência e confere as classificações de confiança baixa com as ferramentas de consulta. Quando muda uma classe, registra o motivo na justificativa.
3. **O código valida e gera.** `validar_documento` recusa conteúdo sem as seções obrigatórias ou com valores fora das listas; `gerar_documento` aplica o modelo visual e mascara segredos.
4. **Amarelo só para incerteza:**

| Vai em amarelo | Não vai em amarelo |
|---|---|
| `[PREENCHER: ...]` (falta dado) | Texto extraído do documento do terceiro |
| Nomes, e-mails, datas e dados pessoais a confirmar | Dados vindos do catálogo TIE, do Swagger e do PL/SQL |
| Inferência da IA e conclusão de confiança média/baixa | Texto padrão do modelo |
| Diagramas gerados | |

## Consequências
- Menos tokens e resultado mais estável: a IA edita um JSON em vez de escrever o documento do zero.
- A classificação automática passa a ser "sugestão com evidência"; a taxa de acerto precisa ser medida com a revisão do consultor.
- O consultor encontra rápido o que é dele, porque o amarelo voltou a significar "olhe aqui".
