# Especificación de datos y reglas

## JSON consolidado (por hoja)
- **Clave principal**: nombre exacto de la hoja.
- **Cada hoja** incluye: `base`, `meta`, `rows`, `audit`.

### Ejemplo
```json
{
  "Hoja_A": {
    "base": "censo_base_1",
    "meta": {
      "filas": 120,
      "columnas": 8,
      "columnas_originales": ["Col_A", "Col_B", "Col_C", "Col_D"],
      "fecha_importacion": "2026-01-28"
    },
    "rows": [
      { "campo_a": "...", "campo_b": 123 },
      { "campo_a": "...", "campo_b": 456 }
    ],
    "audit": {
      "status": "ok",
      "hash_row_policy": "by_index",
      "mismatches": 0,
      "warnings": []
    }
  }
}
```

## Metadatos mínimos
- `filas`, `columnas`
- `columnas_originales`
- `fecha_importacion`
- `base` (seleccionada por el usuario para esa hoja)

## Mapeo por hoja
- Cada hoja tiene su **perfil de mapeo**.
- El perfil conserva el nombre de la hoja y la base asociada.

### Perfil de mapeo (ejemplo)
```json
{
  "sheet": "Hoja_A",
  "base": "censo_base_1",
  "mappings": [
    { "from": "Col_A", "to": "campo_a", "type": "string", "required": true },
    { "from": "Col_B", "to": "campo_b", "type": "number", "required": false }
  ],
  "transformations": [
    { "column": "Col_A", "op": "trim" },
    { "column": "Col_A", "op": "uppercase" },
    { "column": "Col_B", "op": "parse_number" }
  ]
}
```

## Transformaciones soportadas (v1)
- `trim`
- `uppercase` / `lowercase`
- `parse_number`
- `parse_date` (formato configurable)
- `replace` (simple)

## Auditoría
- **Sin ID**: se usa índice de fila + hash normalizado.
- **Hash row**: concatenación de valores normalizados por columna + hashing.
- **Normalización**: trim, tipos básicos (num/texto/fecha), nulos.

### Reporte de auditoría (ejemplo)
```json
{
  "sheet": "Hoja_B",
  "status": "warn",
  "summary": {
    "rows_excel": 55,
    "rows_json": 55,
    "mismatches": 3,
    "nulls": 5
  },
  "details": [
    {
      "row_index": 18,
      "column": "Col_C",
      "excel": "N/A",
      "json": null,
      "reason": "unexpected_null"
    }
  ]
}
```

## Reglas clave
- El **nombre de la hoja** se conserva tal cual en el JSON.
- Auditoría **por hoja** obligatoria antes de exportar.
- El export incluye `audit` por hoja (opcional desactivable).
