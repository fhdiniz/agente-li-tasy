# Formatos usados pelas ferramentas

## 1. conteudo.json (LI e Manual)

```json
{
  "tipo": "li | manual",
  "idioma": "pt-BR | es",
  "capa": { ... },
  "secoes": [
    { "id": "1", "nivel": 1, "titulo": "Objetivo ...", "blocos": [ ... ] },
    { "id": "1.1", "nivel": 2, "titulo": "...", "revisar": true, "blocos": [ ... ] }
  ]
}
```

- `secoes` é uma lista plana, na ordem do documento. `nivel` 1, 2, 3... define a hierarquia. Não escreva o número no título: o gerador numera.
- `id` liga a seção à estrutura oficial (`templates/<tipo>/estrutura.json`). Seções obrigatórias ausentes são erro.
- `"revisar": true` na seção ou no bloco: sai inteiro em amarelo (o consultor valida).
- Seção sem blocos e sem subseções sai como `[PREENCHER: ...]` em amarelo.

Capa da LI: `terceiro`, `software`, `cliente`, `projeto`, `gerente_projeto`, `consultor`, `solicitante`, `registro_id`, `versao`, `classificacao` ("Novo processo", "Alteração" ou "Correções").
Capa do Manual: `titulo`, `codigo`, `revisao`.
Campo de capa vazio fica com o marcador do modelo, em amarelo. Nunca invente nome de pessoa, e-mail ou código.

### Blocos

| Bloco | Exemplo |
|---|---|
| parágrafo | `"texto simples"` ou `{"tipo":"paragrafo","texto":"..."}` |
| subtítulo | `{"tipo":"subtitulo","texto":"..."}` |
| lista | `{"tipo":"lista","numerada":true,"itens":["a","b",{"texto":"sub","nivel":1}]}` |
| tabela | `{"tipo":"tabela","colunas":["A","B"],"linhas":[["1","2"]],"larguras":[30,70]}` |
| código / payload | `{"tipo":"codigo","texto":"{ \"a\": 1 }"}` |
| imagem | `{"tipo":"imagem","arquivo":"telas/tela1.png","legenda":"Figura 1 – ..."}` (caminho relativo à pasta do .docx) |
| diagrama | `{"tipo":"diagrama","modelo":{...}}` (ver item 3) |
| pendência | `{"tipo":"preencher","texto":"o que o consultor deve informar"}` |
| quebra de página | `{"tipo":"quebra_pagina"}` |

### Marcação dentro dos textos

- `**negrito**`, `` `código` ``
- `[[trecho]]`: realce amarelo só no trecho (use em tudo que for inferência, dado pessoal, nome, e-mail ou conclusão de confiança média/baixa)
- `[PREENCHER: o que falta]`: sempre amarelo
- Senhas, tokens e chaves são mascarados automaticamente (`********`). Mesmo assim, não os escreva.

## 2. conteudo.json (CCI)

```json
{
  "tipo": "cci", "idioma": "es | pt-BR",
  "campos": { "titulo": "", "cci_id": "CCI-<CLIENTE>-DD-MM-AAAA", "prioridade": "1 - Alta | 2 - Media | 3 - Baja",
              "cliente": "", "pais": "", "projeto": "", "gerente_bionexo": "", "gerente_cliente": "", "solicitado_por": "",
              "data": "", "integracao": "", "impactara_em": "1 - TIE | 2 - IBE | 3 - TIE/IBE | 4 - Tasy (Producto)",
              "impacto_testes_vendor": "Sí | No | Parcialmente", "impacto_go_live": "Sí | No" },
  "solicitacao": [blocos], "solucao": [blocos], "regras_negocio": [blocos], "comportamento_esperado": [blocos],
  "comportamento_atual": [blocos], "impacto": [blocos], "informacao_adicional": [blocos], "comentarios": [blocos]
}
```

- "Origem da informação no Tasy" e "Componentes com impacto previsto" entram como subtítulo + tabela dentro de `solucao`.
- Esforço, custo e aprovações são do consultor: não preencha (`esforco`, `custo_adicional` ficam de fora).
- Campo vazio fica com o marcador do modelo, em amarelo.

## 3. Modelos de diagrama

A IA descreve; o servidor valida e desenha (.drawio editável + .png).

BPMN (processos e fluxos): raias horizontais, uma por ator/sistema; fluxo da esquerda para a direita; sem loops; cada caminho termina no seu próprio fim. Use até 7 passos por caminho: diagrama mais largo fica ilegível no Word; divida em dois.

```json
{"tipo":"bpmn","titulo":"...","raias":["Tasy","TIE","Terceiro"],
 "nos":[{"id":"i","tipo":"inicio","raia":"Tasy"},{"id":"t1","tipo":"tarefa","raia":"Tasy","texto":"..."},
        {"id":"d1","tipo":"decisao","raia":"TIE","texto":"Aceito?"},{"id":"f1","tipo":"fim","raia":"Terceiro"}],
 "ligacoes":[{"de":"i","para":"t1"},{"de":"d1","para":"f1","texto":"Sim"}]}
```

Casos de uso (UML): `{"tipo":"casos_de_uso","sistema":"Tasy x Terceiro","atores":["Terceiro",{"nome":"Tasy","lado":"direita"}],"casos":[{"nome":"CU01 – ...","atores":["Terceiro","Tasy"]}]}`

Sequência (UML, bom para requisição/resposta): `{"tipo":"sequencia","participantes":["Terceiro","TIE","Tasy"],"mensagens":[{"de":"Terceiro","para":"TIE","texto":"POST ..."},{"de":"TIE","para":"Terceiro","texto":"200","retorno":true}]}`

## 4. requisitos.json (pontos de integração do terceiro)

Lista de objetos, um por ponto de integração. Quando o documento não está no padrão "Resumo / Filtros / SQL", monte a lista você mesmo:

```json
[{ "nome": "CalendarConsultationCheckin", "grupo": "Agenda", "metodo": "PUT", "operacao": "leitura | escrita",
   "resumo": "o que o ponto faz", "filtros": "campos de entrada",
   "tabela_principal": "AGENDA_CONSULTA", "tabelas_escrita": {"AGENDA_CONSULTA": "UPDATE"},
   "tabelas_leitura": [], "colunas": ["AGENDA_CONSULTA.NR_ATENDIMENTO"], "procedures": [], "funcoes": [] }]
```

- Só `nome` e `operacao` são obrigatórios. Quanto mais tabelas e colunas do Tasy você informar, melhor a classificação.
- Se o documento traz SQL, passe-o por `analisar_sql` e copie o resultado para o requisito.
- Se o documento só descreve campos de negócio (sem tabelas), use `buscar_apis` com termos em inglês e informe a tabela que a API encontrada expõe.

## 5. Viabilidade

| Classe | Quando |
|---|---|
| OpenAPI | API padrão cobre o requisito e a maior parte dos campos |
| Parcial | Existe API do assunto, mas faltam campos ou filtros (listar na seção 10 da LI) |
| TIE | Sem API padrão; viável fora do Open por integração TIE (leitura, procedure do Tasy ou evento existente) |
| Gap | Escrita direta em tabela sem API nem procedure: exige desenvolvimento |

A classificação automática é uma sugestão com evidências. Linhas de confiança **Baixa** você confere com `buscar_apis`, `detalhar_api`, `consultar_tabela` e `buscar_tie`; se mudar a classe, edite o `classificacao.json` (campos `classe`, `api`, `justificativa`) antes de gerar o rascunho da LI. A viabilidade fica na matriz interna (.xlsx) e **não vai ao cliente**.
