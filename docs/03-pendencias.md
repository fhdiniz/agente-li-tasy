# Pendências

| Item | Responsável | Status |
|---|---|---|
| Enviar 2 ou 3 LIs de referência (idealmente uma via API REST, uma em português e uma a partir de documento de terceiro) | Fernando | Concluído: template oficial, LIs Baxter e San Javier + 8 LIs do modelo antigo, incluindo 2 via API/JSON (LI10, LI15) |
| Montar o gabarito de testes a partir das LIs assinadas (MANSIS, Pyxis, Bombas, Diverza, LI10, LI15) | Claude | Aberto |
| Enviar template e exemplos de CCI e de manuais (fase 2) | Fernando | Concluído: proposta em [06-modelo-cci-manual](06-modelo-cci-manual.md) |
| Responder os pontos em aberto dos modelos de CCI e Manual | Fernando | Concluído |
| Enviar versões em português dos modelos de LI, CCI e Manual | Fernando | Concluído (Manual PT = mesma estrutura, termos em PT) |
| Documento mestre + referências brutas fora do Git (decisão 0013) | Fernando | Concluído |
| Bases `.docx` por tipo e idioma (LI, CCI, Manual × PT/ES) | Claude | Concluído: `templates/*/base-*.docx` — revisar visualmente no Word |
| Inventário de cobertura (`templates/cobertura.md`) | Claude | Substituído: a cobertura é conferida por `validar_documento` contra `estrutura.json` e pelos testes |
| Coluna de viabilidade da 3.2 | Fernando | Concluído: não vai ao cliente; anexo interno `.xlsx` |
| Enviar os arquivos Swagger | Fernando | Concluído: 51 arquivos, 426 operações |
| Verificar se as descrições do Swagger citam tabela/coluna do Tasy | Claude | Concluído: OpenAPI 3.0.1 traz `Referenced Table`/`Referenced Column`; Swagger 2.0 não |
| Levantar formato do catálogo TIE | Claude | Concluído: 228 integrações em `.bft` (JSON com eventos, rotas Camel e schemas); só 29 têm README |
| De-para tabela → API das APIs em Swagger 2.0 | Claude | Resolvido: extrair do código do tasy-interfaces (`@Table` das entidades JPA) |
| Enviar template visual (.docx) oficial da LI | Fernando | Aberto |
| Informar versão do Tasy e das APIs OpenAPI no cliente do 4uHub | Fernando | Aberto |
| Confirmar se o escopo inclui OPS (`pls_*`) ou só hospitalar | Fernando | Aberto |
| Confirmar autorização para usar Swagger, TIE e LIs com a ferramenta de IA | Eberton | Concluído |
| Confirmar com a TI da Philips se o uv pode ser instalado nas máquinas dos consultores | Eberton | Concluído: liberado (Windows e macOS) |
| Apagar os `.zip` de `referencias/` (índices já extraídos) | Fernando | Aberto |
| Confirmar qual ferramenta de IA será liberada | Eberton | Concluído: Claude, Codex e demais com plugin + MCP (decisão 0009) |
| Migrar repositório da conta do Fernando para a organização da empresa | Fernando / Eberton | Futuro |
| Montar lista de tópicos da LI padrão para validação do grupo | Claude / Fernando | Proposta pronta: [05-modelo-li](05-modelo-li.md) |
| Validar a lista de tópicos e os pontos em aberto do modelo | Fernando | Concluído (19/10/2026), exceto a coluna de viabilidade |
| Gerar inventário estruturado do documento da Evya (prova de conceito) | Claude | Concluído: `mcp-server/agente_li` (extração + classificação), 67 endpoints extraídos, matriz dos 33 de Agenda em `saidas/poc-agenda/` |
| Revisar a matriz de viabilidade da Agenda (colunas do consultor) para medir a taxa de acerto | Fernando | Aberto |
| Reanálise crítica e ajustes gerais | Claude | Concluído (11/2026): [07-reanalise-critica](07-reanalise-critica.md) |
| Gerador de LI, Manual e CCI (.docx), diagramas, servidor MCP, skills e manifestos | Claude | Concluído: `mcp-server/agente_li`, `skills/`, `.claude-plugin`, `.codex-plugin`, `gemini-extension.json` |
| Revisar os 5 documentos de teste em `saidas/testes/` (3 manuais, 1 CCI, 1 LI) no Word | Fernando | Aberto |
| Instalar e testar o plugin no Claude Code, no Codex e no Gemini CLI, em Windows e macOS | Fernando / Claude | Aberto: só Claude Code + uv em Linux foi executado |
| Medir tempo e tokens de uma LI e de um manual feitos pelo plugin, do pedido à revisão | Fernando | Aberto |
| Exportar `.bpmn` para o Bizagi (opcional na decisão 0012) | Claude | Aberto |
| De-para dos mapeamentos do TIE no índice (hoje só os nomes) | Claude | Aberto: exige reextrair o catálogo TIE dos `.bft` originais |
