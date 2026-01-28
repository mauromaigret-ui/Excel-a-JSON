from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Any, Dict, List, Literal, Optional


class SheetInfo(BaseModel):
    name: str
    rows: int
    columns: int
    columns_original: List[str]


class ImportResponse(BaseModel):
    file_id: str
    sheets: List[SheetInfo]


class ColumnMapping(BaseModel):
    from_column: str = Field(..., alias="from")
    to: str
    type: Literal["string", "number", "date", "boolean"] = "string"
    required: bool = False
    default: Optional[Any] = None


class SheetMappingProfile(BaseModel):
    sheet: str
    base: Optional[str] = None
    mappings: List[ColumnMapping]
    include_unmapped: bool = False


class Transformation(BaseModel):
    sheet: str
    column: str
    op: Literal["trim", "uppercase", "lowercase", "parse_number", "parse_date", "replace"]
    args: Optional[Dict[str, Any]] = None


class MapRequest(BaseModel):
    file_id: str
    profiles: List[SheetMappingProfile]
    transformations: List[Transformation] = []
    preview_rows: int = 5


class MapResponse(BaseModel):
    preview: Dict[str, Any]


class AuditRequest(BaseModel):
    file_id: str
    profiles: List[SheetMappingProfile]
    transformations: List[Transformation] = []


class ExportRequest(BaseModel):
    file_id: str
    profiles: List[SheetMappingProfile]
    transformations: List[Transformation] = []
    include_audit: bool = True
    pretty: bool = True


class AuditDetail(BaseModel):
    row_index: int
    column: str
    excel: Any
    json: Any
    reason: str


class AuditSummary(BaseModel):
    rows_excel: int
    rows_json: int
    mismatches: int
    nulls: int


class SheetAudit(BaseModel):
    sheet: str
    status: Literal["ok", "warn", "err"]
    summary: AuditSummary
    details: List[AuditDetail]


class AuditResponse(BaseModel):
    audits: List[SheetAudit]
