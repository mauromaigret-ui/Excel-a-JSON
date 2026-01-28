#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"

if [ ! -d "$BACKEND_DIR" ]; then
  echo "No existe $BACKEND_DIR. Crea el backend primero." >&2
  exit 1
fi

# Backend
if [ -f "$BACKEND_DIR/requirements.txt" ]; then
  if [ ! -d "$BACKEND_DIR/.venv" ]; then
    echo "Creando venv en backend/.venv"
    python3 -m venv "$BACKEND_DIR/.venv"
  fi
  echo "Activando venv e instalando dependencias (si corresponde)"
  source "$BACKEND_DIR/.venv/bin/activate"
  pip install -r "$BACKEND_DIR/requirements.txt"
fi

echo "Arrancando backend..."

# Backend (si existe app/main.py)
if [ -f "$BACKEND_DIR/app/main.py" ]; then
  (source "$BACKEND_DIR/.venv/bin/activate" && uvicorn app.main:app --reload --port 8000)
else
  echo "No se encontró backend/app/main.py; backend no iniciado"
fi
