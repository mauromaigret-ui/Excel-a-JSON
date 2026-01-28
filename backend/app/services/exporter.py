from __future__ import annotations

from typing import Any, Dict, List

import pandas as pd

from app.models.schemas import SheetMappingProfile, Transformation
from app.services.transformer import apply_transformations
from app.services.mapper import build_rows
from app.services.auditor import summarize_audit


def build_consolidated_json(
    sheets: Dict[str, pd.DataFrame],
    profiles: List[SheetMappingProfile],
    transformations: List[Transformation],
    include_audit: bool,
    preview_rows: int | None = None,
) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    transforms_by_sheet: Dict[str, List[Transformation]] = {}
    for t in transformations:
        transforms_by_sheet.setdefault(t.sheet, []).append(t)

    for profile in profiles:
        sheet_name = profile.sheet
        if sheet_name not in sheets:
            continue
        df = sheets[sheet_name]
        df = apply_transformations(df, transforms_by_sheet.get(sheet_name, []))
        rows, audit_details = build_rows(df, profile)
        if preview_rows is not None:
            rows = rows[:preview_rows]

        meta = {
            "filas": int(len(df.index)),
            "columnas": int(len(df.columns)),
            "columnas_originales": [str(c) for c in df.columns.tolist()],
        }

        sheet_obj: Dict[str, Any] = {
            "base": profile.base,
            "meta": meta,
            "rows": rows,
        }

        if include_audit:
            rows_json = len(rows) if preview_rows is None else int(len(df.index))
            audit = summarize_audit(sheet_name, int(len(df.index)), rows_json, audit_details)
            sheet_obj["audit"] = audit.model_dump()

        out[sheet_name] = sheet_obj

    return out
