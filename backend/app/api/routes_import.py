from __future__ import annotations

from fastapi import APIRouter, File, UploadFile, HTTPException

from app.models.schemas import ImportResponse, SheetInfo
from app.services.excel_reader import get_sheets_info
from app.store import store

router = APIRouter()


@router.post("/import", response_model=ImportResponse)
async def import_excel(file: UploadFile = File(...)) -> ImportResponse:
    try:
        content = await file.read()
        stored = store.save_upload(file.filename or "archivo.xlsx", content)
        sheets = get_sheets_info(stored.path)
        return ImportResponse(
            file_id=stored.file_id,
            sheets=[SheetInfo(**s) for s in sheets],
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
