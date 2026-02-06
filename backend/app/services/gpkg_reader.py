from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd

from app.config import GPKG_PATH


def list_layers(gpkg_path: Path = GPKG_PATH) -> List[str]:
    con = sqlite3.connect(gpkg_path)
    try:
        cur = con.cursor()
        cur.execute("SELECT table_name FROM gpkg_contents ORDER BY table_name")
        return [row[0] for row in cur.fetchall()]
    finally:
        con.close()


def get_table_columns(layer: str, gpkg_path: Path = GPKG_PATH) -> List[Tuple[str, str]]:
    con = sqlite3.connect(gpkg_path)
    try:
        cur = con.cursor()
        cur.execute(f"PRAGMA table_info({layer})")
        return [(row[1], row[2]) for row in cur.fetchall()]
    finally:
        con.close()


def load_layer(
    layer: str,
    columns: List[str],
    filter_ids: List[int] | None = None,
    gpkg_path: Path = GPKG_PATH,
) -> pd.DataFrame:
    select_cols = list(dict.fromkeys(columns))
    cols_sql = ", ".join([f'"{c}"' for c in select_cols])
    sql = f"SELECT {cols_sql} FROM {layer}"

    if filter_ids:
        placeholders = ",".join(["?"] * len(filter_ids))
        sql += f" WHERE CAST(ID_ENTIDAD AS INTEGER) IN ({placeholders})"
        params = filter_ids
    else:
        params = None

    con = sqlite3.connect(gpkg_path)
    try:
        df = pd.read_sql_query(sql, con, params=params)
    finally:
        con.close()

    return df


def load_layer_by_names(
    layer: str,
    columns: List[str],
    names: List[Tuple[str, str, str]],
    gpkg_path: Path = GPKG_PATH,
) -> pd.DataFrame:
    # names: list of (ENTIDAD, LOCALIDAD, COMUNA)
    con = sqlite3.connect(gpkg_path)
    try:
        df = pd.read_sql_query(
            f"SELECT {', '.join([f'\"{c}\"' for c in columns])} FROM {layer}",
            con,
        )
    finally:
        con.close()

    if not names:
        return df.iloc[0:0]

    df["ENTIDAD"] = df["ENTIDAD"].astype(str).str.upper().str.strip()
    if "LOCALIDAD" in df.columns:
        df["LOCALIDAD"] = df["LOCALIDAD"].astype(str).str.upper().str.strip()
    if "COMUNA" in df.columns:
        df["COMUNA"] = df["COMUNA"].astype(str).str.upper().str.strip()

    name_set = {(e.upper().strip(), l.upper().strip(), c.upper().strip()) for e, l, c in names}

    def match_row(row: pd.Series) -> bool:
        return (
            row.get("ENTIDAD", "") in [n[0] for n in name_set]
            and ("LOCALIDAD" not in row or row.get("LOCALIDAD", "") in [n[1] for n in name_set])
            and ("COMUNA" not in row or row.get("COMUNA", "") in [n[2] for n in name_set])
        )

    mask = df.apply(match_row, axis=1)
    return df[mask]
