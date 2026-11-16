# 0011 — Formatos de arquivo aceitos

**Status:** Aceita

## Contexto
O documento do terceiro chega em formatos variados. O usuário precisa saber de antemão o que pode enviar e com que qualidade cada formato é lido.

## Decisão

| Formato | Extensões | Leitura | Observação |
|---|---|---|---|
| Documento de texto | `.pdf` (com texto), `.docx`, `.md`, `.txt` | Completa | Formato preferido |
| Especificação de API | `.json`, `.yaml`/`.yml` (OpenAPI/Swagger), `.xml`/`.wsdl`/`.xsd` (SOAP) | Completa e estruturada | Melhor caso: endpoints e campos lidos sem interpretação |
| Exemplos de mensagem | `.json`, `.xml`, `.hl7`, `.txt` | Completa | Ajuda no layout e no mapeamento |
| Planilha | `.xlsx`, `.csv` | Completa | Ex.: planilha de campos/de-para do terceiro |
| Imagem | `.png`, `.jpg` | Pela IA (visão) | Prints de tela, diagramas; confiança menor, itens saem em amarelo |
| PDF escaneado | `.pdf` sem texto | Pela IA (visão), página a página | Mais lento e menos preciso; preferir o original |
| Formatos antigos | `.doc`, `.xls` | Não direto | Salvar como `.docx`/`.xlsx` antes |

**Não aceitos:** links para portais com login, vídeo/áudio, arquivos protegidos por senha. Nesses casos, exportar o conteúdo para um dos formatos acima.

Vários arquivos podem ser enviados juntos (ex.: PDF da especificação + Swagger + exemplos de payload).

## Consequências
- O servidor MCP extrai texto de PDF, DOCX, planilhas e especificações; imagens e PDFs escaneados ficam com o modelo de IA.
- Arquivos em formato não aceito geram aviso com a orientação de conversão, sem interromper os demais.
