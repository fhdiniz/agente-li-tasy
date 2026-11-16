# Guia de uso do plugin

## 1. Antes de começar

1. Instale o **uv** e o plugin na sua ferramenta de IA (ver [README](../README.md)).
2. Crie uma pasta de trabalho, por exemplo `LI-4uHub/`, e coloque nela o documento do terceiro (ou a LI aprovada, para manual e CCI).
3. Abra a ferramenta de IA **nessa pasta**.

## 2. Skills e como chamar

| Skill | Para quê |
|---|---|
| `gerar-li` | Fluxo completo: lê o documento do terceiro, analisa a viabilidade e gera a LI |
| `gerar-manual` | Manual de Integração (modelo EMR 12352) a partir de uma integração do catálogo TIE, de uma API padrão ou de uma LI aprovada |
| `gerar-cci` | CCI no formulário oficial, a partir da descrição da mudança (ata, e-mail, notas) e da LI, se existir |
| `analisar-viabilidade` | Só a matriz de viabilidade (OpenAPI, Parcial, TIE ou Gap), sem gerar a LI |
| `consultar-tasy` | Perguntas pontuais à base de conhecimento. Ex.: "qual API grava em AGENDA_CONSULTA?", "existe integração TIE para cadastro de paciente?" |

### Frase padrão (funciona em qualquer ferramenta)

> **Gere a LI a partir do documento `<arquivo>`.**
> **Gere o manual da integração `<nome>`.** · **Gere o CCI para a mudança `<descrição>`.**
> Também: "analise a viabilidade do documento `<arquivo>`" e "consulte no Tasy `<pergunta>`".

### Atalhos por ferramenta

| Ferramenta | Suporte | Atalho |
|---|---|---|
| Claude Code | Oficial | `/agente-li:gerar-li`, `/agente-li:gerar-manual`, `/agente-li:gerar-cci` |
| Codex | Oficial | `$gerar-li`, `$gerar-manual`, `$gerar-cci` |
| Gemini CLI | Oficial | Frase padrão |
| Cursor, Copilot e outras | Compatível | Frase padrão |

Ver [decisão 0009](decisoes/0009-padrao-multiplataforma.md).

## 3. O que informar

Ao pedir a LI, o agente pede o que estiver faltando. Ter isso em mãos acelera:

| Informação | Exemplo | Por que importa |
|---|---|---|
| **Documento do terceiro** (obrigatório) | Ver formatos aceitos abaixo | É a fonte dos requisitos |
| **Cliente** (obrigatório) | Hospital X | Identificação da LI |
| **Idioma** (obrigatório) | Português ou espanhol | O agente sempre pergunta antes de elaborar |
| **Versão do Tasy** | 1845 | Uma API pode não existir na versão do cliente |
| **Módulos em uso** | Hospitalar, OPS (Plano de Saúde) | Define se itens `pls_*` estão no escopo |
| **Escopo** | Só Agenda e Cadastro | Permite gerar a LI por partes |
| **Restrições** | Cliente não usa TIE; sem acesso direto ao banco | Muda a recomendação |

### Formatos aceitos

| Pode enviar | Observação |
|---|---|
| PDF, DOCX, MD, TXT | Preferidos |
| Swagger/OpenAPI (JSON, YAML), WSDL/XML | Melhor caso: leitura estruturada |
| Exemplos de mensagem (JSON, XML, HL7) | Ajudam no layout e no mapeamento |
| Planilhas (XLSX, CSV) | Ex.: de-para de campos do terceiro |
| Imagens (PNG, JPG) e PDF escaneado | Lidos pela IA; menos precisos — itens saem em amarelo |

Não aceitos: links com login, vídeo/áudio, arquivos com senha. Converta `.doc`/`.xls` para `.docx`/`.xlsx`. Pode enviar vários arquivos juntos. Ver [decisão 0011](decisoes/0011-formatos-de-entrada.md).

## 4. O que o agente entrega

Na pasta de trabalho:

1. **Inventário** dos pontos de integração do terceiro (`requisitos.json`).
2. **Matriz de viabilidade (uso interno, `.xlsx`)** por endpoint, com a API ou integração TIE sugerida, a fonte da conclusão e o nível de confiança. **Não enviar ao cliente.**
3. **LI em .docx** no modelo padrão, com os diagramas em `diagramas/` (`.drawio` editável, que abre no draw.io e no Miro, e `.png`).
4. **Pontos para revisão**: itens de baixa confiança e perguntas ao terceiro ou ao cliente.

Para **Manual** e **CCI**, o agente entrega o `.docx` e o `conteudo.json` que o originou (basta pedir ajustes e gerar de novo).

**O que está em amarelo no documento cabe análise do consultor**: campos a preencher (`[PREENCHER: ...]`), dados a confirmar (nomes, e-mails, versões), inferências da IA e conclusões de confiança média ou baixa. O que veio direto do documento do terceiro ou da base do Tasy não é marcado ([decisão 0014](decisoes/0014-rascunho-em-codigo-ia-revisa.md)). A resposta do agente lista esses itens por seção. Ver [decisão 0010](decisoes/0010-destaque-revisao-consultor.md).

## 5. Revisão

O consultor revisa os itens em amarelo e os pontos da lista 4, responde no próprio chat (ex.: "o endpoint 12 é coberto pela API X, ajuste") e pede para regerar a LI. A LI só é enviada ao cliente depois dessa revisão e sem nenhum realce amarelo.

## Exemplo

```
Gere a LI a partir do documento "Documentação Integração TASY e Portal 4uHub.pdf".
Cliente: Hospital X | Versão: 1845 | Módulos: Hospitalar | Escopo: Agenda e Cadastro
```

Manual e CCI:

```
Gere o manual da integração URA Avaya, em português.
Gere o CCI, em espanhol, para ativar o envio do Código de Deudor na integração de Persona Física. Cliente: Hospital X.
```
