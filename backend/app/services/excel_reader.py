from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import pandas as pd


def list_sheets(file_path: Path) -> List[str]:
    xls = pd.ExcelFile(file_path)
    return xls.sheet_names


def read_sheet(file_path: Path, sheet_name: str) -> pd.DataFrame:
    df = pd.read_excel(file_path, sheet_name=sheet_name, dtype=object)
    df = df.where(pd.notna(df), None)
    return df


def get_sheets_info(file_path: Path) -> List[Dict[str, object]]:
    sheets = []
    for name in list_sheets(file_path):
        df = read_sheet(file_path, name)
        sheets.append(
            {
                "name": name,
                "rows": int(len(df.index)),
                "columns": int(len(df.columns)),
                "columns_original": [str(c) for c in df.columns.tolist()],
            }
        )
    return sheets
