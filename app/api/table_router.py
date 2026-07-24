from fastapi import APIRouter
from fastapi import HTTPException

from app.schemas.pdf_request import PDFRequest
from app.services.pdf_extraction_service import extract_pdf

router = APIRouter()


@router.post("/extract-table")
async def extract_table(request: PDFRequest):

    try:

        return extract_pdf(request)

    except HTTPException:

        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )