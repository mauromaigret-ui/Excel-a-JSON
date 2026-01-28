from __future__ import annotations

import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from app.models.schemas import ExportRequest
from app.services.excel_reader import read_sheet
from app.services.exporter import build_consolidated_json
from app.store import store

router = APIRouter()


@router.post("/export")
def export_json(req: ExportRequest) -> Response:
    try:
        stored = store.get(req.file_id)
        sheets = {profile.sheet: read_sheet(stored.path, profile.sheet) for profile in req.profiles}
        payload = build_consolidated_json(
            sheets,
            req.profiles,
            req.transformations,
            include_audit=req.include_audit,
            preview_rows=None,
        )
        if req.pretty:
            body = json.dumps(payload, ensure_ascii=False, indent=2)
        else:
            body = json.dumps(payload, ensure_ascii=False)
        return Response(content=body, media_type="application/json")
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
