from __future__ import annotations

from typing import List

import pandas as pd

from app.models.schemas import Transformation


def apply_transformations(df: pd.DataFrame, transformations: List[Transformation]) -> pd.DataFrame:
    if not transformations:
        return df

    df = df.copy()
    for t in transformations:
        if t.column not in df.columns:
            continue
        series = df[t.column]
        if t.op == "trim":
            df[t.column] = series.apply(lambda v: v.strip() if isinstance(v, str) else v)
        elif t.op == "uppercase":
            df[t.column] = series.apply(lambda v: v.upper() if isinstance(v, str) else v)
        elif t.op == "lowercase":
            df[t.column] = series.apply(lambda v: v.lower() if isinstance(v, str) else v)
        elif t.op == "parse_number":
            df[t.column] = pd.to_numeric(series, errors="coerce")
        elif t.op == "parse_date":
            fmt = (t.args or {}).get("format")
            df[t.column] = pd.to_datetime(series, errors="coerce", format=fmt)
        elif t.op == "replace":
            args = t.args or {}
            old = args.get("old")
            new = args.get("new")
            if old is not None:
                df[t.column] = series.replace(old, new)
    df = df.where(pd.notna(df), None)
    return df
