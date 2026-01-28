from __future__ import annotations

from typing import Any, Dict, List, Tuple

import pandas as pd

from app.models.schemas import ColumnMapping, SheetMappingProfile


def normalize_value(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, str):
        value = value.strip()
        return value if value != "" else None
    if pd.isna(value):
        return None
    if hasattr(value, "to_pydatetime"):
        return value.to_pydatetime().isoformat()
    return value


def convert_type(value: Any, target_type: str) -> Tuple[Any, bool]:
    if value is None:
        return None, False
    try:
        if target_type == "string":
            return str(value), False
        if target_type == "number":
            num = pd.to_numeric(value, errors="coerce")
            if pd.isna(num):
                return None, True
            if float(num).is_integer():
                return int(num), False
            return float(num), False
        if target_type == "date":
            dt = pd.to_datetime(value, errors="coerce")
            if pd.isna(dt):
                return None, True
            return dt.to_pydatetime().date().isoformat(), False
        if target_type == "boolean":
            if isinstance(value, bool):
                return value, False
            if isinstance(value, (int, float)):
                return bool(value), False
            if isinstance(value, str):
                v = value.strip().lower()
                if v in {"true", "1", "yes", "si"}:
                    return True, False
                if v in {"false", "0", "no"}:
                    return False, False
            return None, True
    except Exception:
        return None, True
    return value, False


def build_rows(
    df: pd.DataFrame,
    profile: SheetMappingProfile,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    mappings = profile.mappings
    mapped_columns = {m.from_column for m in mappings}
    rows: List[Dict[str, Any]] = []
    audit_details: List[Dict[str, Any]] = []

    for row_index, row in df.iterrows():
        out: Dict[str, Any] = {}
        for m in mappings:
            raw = row.get(m.from_column)
            normalized = normalize_value(raw)
            converted, conversion_failed = convert_type(normalized, m.type)

            if converted is None and m.default is not None:
                converted = m.default

            if conversion_failed:
                audit_details.append(
                    {
                        "row_index": int(row_index),
                        "column": m.from_column,
                        "excel": raw,
                        "json": converted,
                        "reason": "conversion_failed",
                    }
                )

            if converted is None and m.required:
                audit_details.append(
                    {
                        "row_index": int(row_index),
                        "column": m.from_column,
                        "excel": raw,
                        "json": converted,
                        "reason": "missing_required",
                    }
                )

            out[m.to] = converted

        if profile.include_unmapped:
            for col in df.columns:
                if col in mapped_columns:
                    continue
                raw = row.get(col)
                out[str(col)] = normalize_value(raw)

        rows.append(out)

    return rows, audit_details


def default_profile_from_columns(sheet: str, columns: List[str]) -> SheetMappingProfile:
    mappings = [
        ColumnMapping(from_column=str(c), to=str(c), type="string")
        for c in columns
    ]
    return SheetMappingProfile(sheet=sheet, mappings=mappings)
