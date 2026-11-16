# Reanálise crítica e ajustes (novembro de 2026)

Revisão geral do projeto antes de validar a geração de LI, Manual e CCI. O que estava errado ou faltando, o que foi feito e o que continua em aberto.

## O que a reanálise encontrou

| # | Problema | Efeito | O que foi feito |
|---|---|---|---|
| 1 | Não existia gerador de documento: só modelos e estrutura | A meta das 8h não era testável | `agente_li/documento.py` gera LI, Manual e CCI em `.docx` sobre as bases |
| 2 | Não existia plugin instalável (sem servidor MCP, skills nem manifestos) | Ninguém além do autor conseguia usar | Servidor MCP (16 ferramentas), 5 skills, manifestos para Claude Code, Codex e Gemini CLI |
| 3 | Leitura de PDF dependia do `pdftotext`, que não existe no Windows | Quebraria na máquina dos consultores | Trocado por `pypdf` (puro Python) |
| 4 | O extrator só entende documentos no padrão da Evya | Qualquer outro terceiro travaria | Contrato comum `requisitos.json`: a IA monta quando o extrator não se aplica; `analisar_sql` e `ler_documento` ajudam |
| 5 | Classificação com vocabulário só de Agenda, em inglês, e sem conferência | Resultado frágil fora do caso Evya | Vocabulário PT/ES; a classificação virou sugestão com evidências e a IA confere as linhas de confiança baixa (decisão 0014) |
| 6 | Manual e CCI eram só proposta de estrutura | Demanda de manuais sem ferramenta | Rascunho automático do Manual a partir do catálogo TIE ou do Swagger; CCI preenchido no formulário oficial |
| 7 | Diagramas só existiam como decisão | LI sem fluxos | `agente_li/diagrama.py`: BPMN, casos de uso e sequência, com as regras da equipe; entrega `.drawio` + `.png` |
| 8 | Mascaramento de senhas era só regra escrita | Risco de credencial no documento | O gerador mascara segredos em todo texto e código |
| 9 | "Tudo que é rascunho sai em amarelo" deixaria o documento inteiro amarelo | O amarelo perderia o sentido | Amarelo só para pendência, inferência e baixa confiança (decisão 0014) |
| 10 | Bases `.docx` com XML fora da ordem do Word (campo de atualização do sumário) | Risco de aviso de arquivo corrompido | Bases regeradas; todos os documentos de teste passam na validação de schema |
| 11 | Formulário do CCI: lista de esforço com faixas de horas em Média/Baixa, sem "4 - Tasy (Producto)", rodapé em inglês | Diferente do combinado | Corrigido nas bases |
| 12 | Índice de eventos do TIE não achava alguns gatilhos (ex.: `api.pf_codigo_externo.send`) | Manual sem o gatilho | Busca pelo nome da trigger como segunda opção, marcada "a confirmar" |
| 13 | Índice OpenAPI guardava só tabela/coluna | Sem de-para de campos | Índice passa a guardar cada tag JSON com tipo, obrigatoriedade, tabela e coluna |
| 14 | Documentação desatualizada (classes, ferramentas, estrutura) | Confunde quem chega | README, AGENTS, arquitetura, guia e pendências revisados |

## Testes feitos (em `saidas/testes/`, fora do Git)

| Documento | Fonte | Idioma | Resultado |
|---|---|---|---|
| Manual "Persona Física – SAP MDM" | `.bft` da integração natural-person (TIE) + README | es | 10 páginas |
| Manual "URA Avaya" | `.bft` ura-avaya (TIE chamando APIs do Tasy) | pt-BR | 10 páginas |
| Manual "API Agenda de Consultas" | Swagger Consultation Schedule | pt-BR | 28 páginas, de-para de tags por operação |
| CCI "Código de Deudor" | catálogo TIE (rota desativada no pacote) | es | 3 páginas |
| LI Evya Portal 4uHub — Agenda | PDF da Evya, 33 pontos | pt-BR | 58 páginas + matriz interna `.xlsx` |

Tempo de máquina: cerca de 10 s para a LI (leitura do PDF incluída) e menos de 2 s para cada manual. O tempo da IA para redigir e do consultor para revisar ainda não foi medido em uso real.

## Limites conhecidos

- **Taxa de acerto da viabilidade ainda não medida**: a matriz da Agenda aguarda a revisão do consultor. Sem isso não há como afirmar que a classificação é confiável.
- **Manuais do TIE**: o catálogo traz os nomes dos mapeamentos, não o de-para dos campos, nem telas e parâmetros funcionais do Tasy. Esses itens saem como `[PREENCHER]`.
- **Diagramas largos** (mais de ~7 passos em linha) ficam pequenos no Word; o `.drawio` é o editável. `.bpmn` para o Bizagi não foi implementado.
- **Conferido no LibreOffice e por validação de schema**, não no Word nem em Windows.
- **Manifestos do Codex e do Gemini CLI** seguem a documentação pública, mas não foram testados nessas ferramentas. Só o caminho Claude Code + uv foi executado de ponta a ponta.
- **Arquitetura do cliente** (seção 4 da LI) e telas do Tasy continuam manuais.
