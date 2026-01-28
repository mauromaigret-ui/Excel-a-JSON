# Backend (local)

Servidor local para importar Excel, mapear, transformar, auditar y exportar JSON.

## Requisitos
- Python 3.11+

## Inicio rápido
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Luego abre `http://localhost:8000` en el navegador.
