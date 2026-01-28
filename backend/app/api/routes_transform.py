from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.models.schemas import MapRequest, MapResponse
from app.services.excel_reader import read_sheet
from app.services.exporter import build_consolidated_json
from app.store import store

router = APIRouter()


@router.post("/transform", response_model=MapResponse)
def transform_preview(req: MapRequest) -> MapResponse:
    try:
        stored = store.get(req.file_id)
        sheets = {profile.sheet: read_sheet(stored.path, profile.sheet) for profile in req.profiles}
        preview = build_consolidated_json(
            sheets,
            req.profiles,
            req.transformations,
            include_audit=False,
            preview_rows=req.preview_rows,
        )
        return MapResponse(preview=preview)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
