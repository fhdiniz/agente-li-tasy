# Extratores

Scripts (Python, só biblioteca padrão) que geram `referencias/indices/` a partir dos repositórios internos. Rodar nesta ordem:

```bash
python extrair_interfaces.py <tasy-interfaces> ../../referencias/indices/interfaces
python extrair_tie.py        <tie-integrations> ../../referencias/indices/tie
# lista de tabelas JPA para filtrar leituras do PL/SQL
python -c "import json;json.dump(list(json.load(open('../../referencias/indices/interfaces/entidades.json'))),open('/tmp/jpa.json','w'))"
python extrair_plsql.py      <emr-tasy-plsql>   ../../referencias/indices/plsql /tmp/jpa.json
python montar_indice_tabelas.py ../../referencias
```

`montar_indice_tabelas.py` não depende dos repositórios: pode ser reexecutado sempre que os Swaggers mudarem.
