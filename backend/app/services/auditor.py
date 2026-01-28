from __future__ import annotations

from typing import Any, Dict, List

from app.models.schemas import AuditDetail, AuditSummary, SheetAudit


def summarize_audit(sheet: str, rows_excel: int, rows_json: int, audit_details: List[Dict[str, Any]]) -> SheetAudit:
    mismatches = len(audit_details)
    nulls = sum(1 for d in audit_details if d.get("json") is None)

    if mismatches == 0 and rows_excel == rows_json:
        status = "ok"
    elif mismatches <= 5 and rows_excel == rows_json:
        status = "warn"
    else:
        status = "err"

    details = [AuditDetail(**d) for d in audit_details]
    summary = AuditSummary(
        rows_excel=rows_excel,
        rows_json=rows_json,
        mismatches=mismatches,
        nulls=nulls,
    )
    return SheetAudit(sheet=sheet, status=status, summary=summary, details=details)
