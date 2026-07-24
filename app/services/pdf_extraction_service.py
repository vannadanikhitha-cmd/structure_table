import os
import base64
import tempfile
import traceback
from fastapi import HTTPException

from app.schemas.pdf_request import PDFRequest

from app.processors.hybrid_pdf_processor import process_hybrid_pdf

from app.extractors.transaction_extractor import (
    extract_transactions
)


def extract_pdf(request: PDFRequest):

    pdf_path = None

    try:

        # ------------------------------------
        # Decode Base64 PDF
        # ------------------------------------

        pdf_bytes = base64.b64decode(
            request.pdf_base64
        )

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_pdf:

            temp_pdf.write(pdf_bytes)

            pdf_path = temp_pdf.name

        print("=" * 60)
        print("Temporary PDF Created")
        print(pdf_path)
        print("=" * 60)

        # ------------------------------------
        # Hybrid Processor
        # (Outside data + OCR Validation)
        # ------------------------------------

        table_data, outside_data = process_hybrid_pdf(
            pdf_path
        )

        print("Hybrid Processor Completed")

        # ------------------------------------
        # Structured Extraction
        # (Axis + SBI + HDFC)
        # ------------------------------------

        # table_data = extract_transactions(
        #     pdf_path
        # )

        if not table_data:

            raise HTTPException(
                status_code=404,
                detail="No data found in PDF"
            )

        return {

            "status": "success",

            "file_name": request.file_name,

            "outside_data": outside_data,

            "table_data": table_data
        }

    except HTTPException:

        raise

    except Exception as e:
        print("=" * 80)
        traceback.print_exc()
        print("=" * 80)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:

        if pdf_path and os.path.exists(pdf_path):

            os.remove(pdf_path)

            print("Temporary File Deleted")