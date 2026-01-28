from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.models.schemas import AuditRequest, AuditResponse
from app.services.excel_reader import read_sheet
from app.services.transformer import apply_transformations
from app.services.mapper import build_rows
from app.services.auditor import summarize_audit
from app.store import store

router = APIRouter()


@router.post("/audit", response_model=AuditResponse)
def audit(req: AuditRequest) -> AuditResponse:
    try:
        stored = store.get(req.file_id)
        audits = []
        transforms_by_sheet = {}
        for t in req.transformations:
            transforms_by_sheet.setdefault(t.sheet, []).append(t)

        for profile in req.profiles:
            df = read_sheet(stored.path, profile.sheet)
            df = apply_transformations(df, transforms_by_sheet.get(profile.sheet, []))
            rows, audit_details = build_rows(df, profile)
            audits.append(
                summarize_audit(
                    profile.sheet,
                    rows_excel=int(len(df.index)),
                    rows_json=int(len(rows)),
                    audit_details=audit_details,
                )
            )

        return AuditResponse(audits=audits)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
