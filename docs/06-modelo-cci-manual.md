# Modelos de CCI e Manual (fase 2 — proposta)

> Proposta para validação. Estruturas de máquina: [`templates/cci/estrutura.json`](../templates/cci/estrutura.json) e [`templates/manual/estrutura.json`](../templates/manual/estrutura.json). Os três documentos usam o mesmo motor da LI (decisão 0003).

## Como os documentos se encadeiam

```
LI (levantamento) ──aprovada──▶ CCI (cada mudança depois da aprovação)
        │                              │
        └──────── implantação ─────────┴──▶ Manual de Integração (como configurar e operar)
```

A LI é a fonte principal: o CCI compara a mudança com o que a LI aprovou; o manual reaproveita casos de uso, fluxos, mapeamentos e casos de teste da LI.

## CCI — Control de Cambio de Integración

**Bases:** template `CCI Template Control de cambios integraciones_Bionexo_Tasy.docx` (já vem preenchido com um exemplo: BackOffice Finanzas) e três CCIs reais (TecSalud/Diverza, ABC/Pyxis e TecSalud/Banco de Sangre). Todos seguem a mesma estrutura.

- O CCI serve tanto para **alteração** quanto para **ampliação de escopo** (Banco de Sangre: novo fluxo de hemocomponentes, HL7 OMB^O27).
- O template usa **listas suspensas do Word** ("Elija un elemento") em prioridade, impacto, esforço e custo: o gerador do `.docx` precisa preencher esses controles, não só texto.

| Seção | Conteúdo | Preenchimento |
|---|---|---|
| Cabeçalho | Título, ID (`CCI-<CLIENTE>-DD-MM-AAAA`), prioridade, cliente, país, projeto, GPs, solicitante, data, integração, "impactará em", impacto em testes do vendor e no Go Live | Rascunho |
| Solicitação de mudança | Contexto, necessidade, decisões da sessão, condicionantes | Rascunho |
| Solução proposta | Regras de negócio · comportamento esperado · comportamento atual · origem no Tasy (tabela.campo, tipo, JSON, destino) · componentes impactados (templates TIE, APIs) · impacto | Rascunho |
| Informação adicional | Evidências e pendências de confirmação | Auto |
| Avaliação de impacto | Esforço (complexidade × horas) e custo adicional | **Manual** |
| Comentários adicionais | — | Rascunho |
| Aprovações | Cliente e Bionexo Tasy (aprovado/rejeitado, nome, data, assinatura) | **Manual** |

**O que o agente agrega:** a partir da ata/e-mail da mudança e da LI aprovada, aponta o caso de uso afetado, a origem do dado no Tasy (ex.: `NOTA_FISCAL.DS_OBSERVACAO`, VARCHAR2 4000) e os componentes TIE a ajustar (ex.: tabela por transformação HL7, como no CCI Pyxis). Esforço e custo ficam sempre com o consultor.

## Manual de Integração (MO — modelo EMR 12352)

**Bases:** modelo oficial `EMR 12352 MO - Modelo para Manual de Integración_009_ES.docx`, o manual do Copiloto Médico (TecSalud) e os 13 manuais oficiais do TIE já na base (`indices/tie/manuais/`).

| Seção | Conteúdo | Preenchimento |
|---|---|---|
| Aviso | Texto fixo de propriedade Bionexo Tasy | Auto |
| 1 Objetivo | Características, público, **dados pessoais e sensíveis** | Auto / Rascunho |
| 2 Requisitos | Infraestrutura e sistema (cadastros/funções do Tasy) | Rascunho |
| 3 Fluxo | Passo a passo da integração | Rascunho |
| 4 Configurações | Forma de comunicação; cadastros e parametrizações — para TIE: conector, evento, fluxo, rota e mapeamento | Rascunho |
| 5 Testes | Processo e visualização dos resultados | Rascunho (telas: manual) |

**O que o agente agrega:** a seção 1.3 (dados pessoais e sensíveis) sai automática a partir do mapeamento da LI; a 4.2 pode ser preenchida com a configuração real da integração no catálogo TIE (conector, eventos, rotas, fluxos), no formato do manual oficial "MI - API Atendimentos".

## Definições (confirmadas por Fernando em 19/10/2026)

| Item | Valores |
|---|---|
| CCI — "Cambio impactará en" | 1 - TIE · 2 - IBE · 3 - TIE/IBE · 4 - Tasy (Producto) |
| CCI — Prioridade do cliente | 1 - Alta · 2 - Média · 3 - Baixa |
| CCI — Esforço (complexidade) | 1 - Alta (>60h) · 2 - Média · 3 - Baixa (só a Alta tem faixa de horas definida) |
| Manual | Base única: modelo **EMR 12352**. Para integrações via TIE, a seção 4.2 inclui conector, evento, fluxo, rota, mapeamentos e parâmetros — quanto mais detalhe, melhor |

## Pontos em aberto

1. **Idioma:** recebidos em PT a LI (EMR 0198, mesmo layout do template) e um "Controle de Mudanças do Projeto" (documento de projeto, mais simples que o CCI de integração). Decisão: manter as estruturas atuais e usar os PT só para os títulos e termos em português. O Manual em PT tem a mesma estrutura do EMR 12352, só com os termos em português.
