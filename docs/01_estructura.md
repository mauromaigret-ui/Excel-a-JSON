# Estructura de carpetas (propuesta)

```
.
├─ backend/
│  ├─ app/
│  │  ├─ main.py
│  │  ├─ api/
│  │  │  ├─ routes_import.py
│  │  │  ├─ routes_map.py
│  │  │  ├─ routes_transform.py
│  │  │  ├─ routes_audit.py
│  │  │  └─ routes_export.py
│  │  ├─ services/
│  │  │  ├─ excel_reader.py
│  │  │  ├─ mapper.py
│  │  │  ├─ transformer.py
│  │  │  ├─ auditor.py
│  │  │  └─ exporter.py
│  │  ├─ models/
│  │  │  ├─ schemas.py
│  │  │  └─ audit_models.py
│  │  └─ store/
│  │     ├─ history.json
│  │     └─ profiles/
│  ├─ requirements.txt
│  └─ README.md
├─ frontend/
│  ├─ index.html
│  ├─ static/
│  │  ├─ app.js
│  │  └─ styles.css
│  └─ README.md
├─ docs/
│  ├─ 01_estructura.md
│  ├─ 02_wireframes.md
│  ├─ 03_especificacion_datos.md
│  └─ 04_flujo_y_endpoints.md
└─ run_local.sh
```

## Racional
- **backend/**: servidor local para leer Excel, mapear, transformar, auditar y exportar JSON.
- **frontend/**: interfaz web en navegador (localhost), servida por FastAPI.
- **docs/**: especificaciones de diseño y datos.
- **run_local.sh**: arranque rápido local.

## Notas
- `store/` guarda historial y perfiles de mapeo por hoja.
- Se conserva el **nombre exacto de cada hoja** en el JSON consolidado.
