# Wireframes (detallados)

## 1) Importar + Selección de hojas

```
┌────────────────────────────────────────────────────────────────────────────┐
│ Proyecto: Censo 2024  | Archivo: (sin cargar)                    [Historial]│
├────────────────────────────────────────────────────────────────────────────┤
│ PASOS                              |                                      │
│ 1. Importar  ●                     |  Arrastra tu Excel o selecciona       │
│ 2. Hojas                           |  ┌─────────────────────────────────┐   │
│ 3. Mapeo                           |  │   Dropzone + botón elegir        │   │
│ 4. Transformar                     |  └─────────────────────────────────┘   │
│ 5. Vista JSON                      |                                      │
│ 6. Auditoría                       |  Hojas detectadas:                    │
│ 7. Exportar                        |  [ ] Hoja_A   (120x8)                 │
│                                    |  [ ] Hoja_B   (55x5)                  │
│                                    |  [ ] Hoja_C   (300x12)                │
│                                    |                                      │
│                                    |  [Continuar]                          │
└────────────────────────────────────────────────────────────────────────────┘
```

## 2) Mapeo por hoja

```
┌────────────────────────────────────────────────────────────────────────────┐
│ Hoja: Hoja_A  | Base: [censo_base_1 ▼]                   [Guardar perfil]  │
├────────────────────────────────────────────────────────────────────────────┤
│ TABLA (Excel)                         | ESQUEMA JSON                         │
│ ┌──────────────────────────────────┐ | ┌──────────────────────────────────┐ │
│ │ Col_A | Col_B | Col_C | Col_D    │ | │ root.Hoja_A.rows[]                │ │
│ │  ...  |  ...  |  ...  |  ...     │ | │  • campo_a  <- Col_A              │ │
│ │       |       |       |          │ | │  • campo_b  <- Col_B              │ │
│ └──────────────────────────────────┘ | │  • campo_c  <- Col_C              │ │
│                                      | │  • campo_d  <- Col_D              │ │
│                                      | └──────────────────────────────────┘ │
│                                                                              │
│ Reglas rápidas: [Renombrar] [Tipo] [Default] [Obligatorio] [Trim]            │
└────────────────────────────────────────────────────────────────────────────┘
```

## 3) Transformaciones

```
┌────────────────────────────────────────────────────────────────────────────┐
│ Hoja: Hoja_A | Transformaciones                                              │
├────────────────────────────────────────────────────────────────────────────┤
│ Columna      | Transformación           | Preview (5 filas)                 │
│ Col_A        | trim + uppercase         | ...                               │
│ Col_B        | parse_number             | ...                               │
│ Col_C        | parse_date(DD/MM/YYYY)   | ...                               │
└────────────────────────────────────────────────────────────────────────────┘
```

## 4) Vista JSON

```
┌────────────────────────────────────────────────────────────────────────────┐
│ Vista JSON (consolidado)                                   [Pretty ▼]       │
├────────────────────────────────────────────────────────────────────────────┤
│ {                                                                          │
│   "Hoja_A": {                                                             │
│     "base": "censo_base_1",                                              │
│     "meta": {"filas": 120, "columnas": 8},                             │
│     "rows": [ { ... }, { ... } ]                                         │
│   },                                                                       │
│   "Hoja_B": { ... }                                                       │
│ }                                                                          │
└────────────────────────────────────────────────────────────────────────────┘
```

## 5) Auditoría

```
┌────────────────────────────────────────────────────────────────────────────┐
│ Auditoría por hoja                                                           │
├────────────────────────────────────────────────────────────────────────────┤
│ Hoja_A  [OK]     filas:120  mismatches:0                                    │
│ Hoja_B  [WARN]   filas:55   mismatches:3   [Ver detalle]                    │
│ Hoja_C  [ERR]    filas:300  mismatches:12  [Ver detalle]                    │
│                                                                            │
│ Detalle (Hoja_B)                                                            │
│ Fila | Columna | Valor Excel | Valor JSON | Tipo | Estado                   │
│  12  | col_B   | " 23"      | 23         | num  | normalizado              │
│  18  | col_C   | "N/A"      | null       | txt  | nulo inesperado           │
└────────────────────────────────────────────────────────────────────────────┘
```

## 6) Exportar

```
┌────────────────────────────────────────────────────────────────────────────┐
│ Exportar JSON consolidado                                                    │
├────────────────────────────────────────────────────────────────────────────┤
│ Nombre de archivo: [censo_2024.json]                                        │
│ Formato: [Pretty ▼]   |   Incluir auditoría: [x]                            │
│                                                                            │
│ [Descargar JSON]   [Copiar]   [Guardar reporte auditoría]                  │
└────────────────────────────────────────────────────────────────────────────┘
```
