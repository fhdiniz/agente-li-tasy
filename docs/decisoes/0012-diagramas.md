# 0012 — Diagramas gerados por código a partir de um modelo

**Status:** Aceita

## Contexto
A LI exige diagramas (casos de uso, mapa do processo, fluxo por caso de uso) com padrão de modelagem definido pela equipe. A equipe já usou Bizagi e hoje usa Miro. Não existe um formato editável único aceito pelos dois: o Bizagi importa **BPMN 2.0 XML**; o Miro importa **.vsdx** (Visio) e tem integração com draw.io, mas não importa BPMN.

## Decisão
1. A IA monta um **modelo do diagrama em JSON** (raias, nós, eventos, ligações). Ela não desenha.
2. O servidor MCP **valida** o modelo contra o padrão da equipe e recusa o que violar:
   - BPMN para fluxos e processos; UML para casos de uso e sequência;
   - raias horizontais, uma por ator/sistema;
   - fluxo da esquerda para a direita;
   - formas de tamanho uniforme;
   - sem loops inválidos;
   - cada caminho termina no seu próprio evento de fim (sem juntar terminais).
3. O MCP **desenha** (layout determinístico) e entrega:

| Arquivo | Para quê | Abre em | Status |
|---|---|---|---|
| `.drawio` | **Formato editável oficial** de todos os diagramas (BPMN e UML) | draw.io (gratuito, web e desktop); **no Miro direto**, pelo app "Draw.io diagrams by Miro" (todos os planos), ou via export `.vsdx` | **Mandatório** |
| `.png` | Imagem inserida no `.docx`, legenda "diagrama gerado — revisar" em amarelo (decisão 0010) | Word | Mandatório |
| `.json` | Modelo original, reaproveitável em outra ferramenta ou IA | — | Mandatório |
| `.bpmn` (BPMN 2.0 com coordenadas) | Abrir fluxos e processos no Bizagi | Bizagi, Camunda Modeler, bpmn.io | Opcional |

**Por que o `.bpmn` continua existindo:** o draw.io **não exporta BPMN 2.0** (os mantenedores recusaram esse recurso) e o Bizagi só importa BPMN 2.0/XPDL. Como o `.bpmn` é gerado pelo mesmo modelo JSON, não custa nada para o consultor; quem não usa Bizagi ignora.

| Seção da LI | Diagrama |
|---|---|
| 3.2 Casos de uso | UML de caso de uso |
| 5 Mapa do processo | BPMN com raias por ator |
| 6.n Fluxo do caso de uso | BPMN com raias por sistema (ou UML de sequência para request/response) |
| 4 Arquitetura | Rascunho; o consultor completa |

## Consequências
- Mesmo padrão visual em todas as LIs, independente de quem gera.
- draw.io é a ferramenta mandatória de edição; no Miro, o `.drawio` abre direto pelo app oficial "Draw.io diagrams by Miro".
- Editar no draw.io não atualiza o `.bpmn`: para Bizagi, editar no próprio Bizagi.
- O desenho é feito em Python (sem Java/Node), mantendo a premissa da decisão 0007.
