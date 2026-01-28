# Flujo funcional y endpoints (backend local)

## Flujo funcional
1) **Importar Excel**
   - Se lee el archivo y se listan hojas con tamaño y columnas.
2) **Seleccionar hojas**
   - El usuario elige una o varias.
3) **Mapeo por hoja**
   - Mapeo columna → campo JSON y base asociada.
4) **Transformaciones**
   - Se aplican reglas simples por columna.
5) **Vista JSON**
   - Preview del JSON consolidado.
6) **Auditoría**
   - Comparación hoja por hoja y reporte.
7) **Exportar**
   - Descarga de JSON consolidado + reporte de auditoría.

## Endpoints sugeridos
- `POST /import`
  - input: archivo Excel
  - output: hojas detectadas + columnas + tamaños

- `POST /map`
  - input: perfil de mapeo por hoja
  - output: preview de filas mapeadas

- `POST /transform`
  - input: reglas de transformación
  - output: preview transformado

- `POST /audit`
  - input: JSON consolidado + tabla original
  - output: reporte de auditoría por hoja

- `GET /export`
  - output: JSON consolidado (opcional con auditoría)

## Consideraciones técnicas
- Backend en **Python + FastAPI**.
- Lectura Excel con `pandas` + `openpyxl`.
- Auditoría por hoja usando hash por fila (sin ID).
