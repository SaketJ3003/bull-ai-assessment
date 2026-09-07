import os
import uuid

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse

from app.services.gemini_service import GeminiService
from app.services.mapper import map_gemini_to_financial_report
from app.pdf.generator import FinancialReportPDF


router = APIRouter(prefix="/api", tags=["reports"])

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

UPLOAD_DIR = os.path.join(
    BASE_DIR,
    "generated",
    "uploads"
)

REPORT_DIR = os.path.join(
    BASE_DIR,
    "generated",
    "reports"
)

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)


ALLOWED_EXTENSIONS = {
    ".pdf",
    ".csv",
    ".txt",
}

MAX_FILE_SIZE = 50 * 1024 * 1024


def friendly_error(exc: Exception) -> tuple[int, str]:
    """
    Convert technical backend/API errors into user-friendly
    messages without exposing implementation details.
    """

    message = str(exc).lower()

    # Gemini temporary availability / high demand
    if any(
        keyword in message
        for keyword in [
            "503",
            "unavailable",
            "high demand",
            "service unavailable",
        ]
    ):
        return (
            503,
            "The AI service is temporarily busy. "
            "Please try again in a moment."
        )

    # Gemini rate limiting
    if any(
        keyword in message
        for keyword in [
            "429",
            "rate limit",
            "resource exhausted",
            "too many requests",
        ]
    ):
        return (
            429,
            "The AI service is currently rate-limited. "
            "Please wait a moment and try again."
        )

    # Invalid Gemini request
    if any(
        keyword in message
        for keyword in [
            "400",
            "invalid_argument",
            "invalid argument",
        ]
    ):
        return (
            400,
            "The uploaded document could not be processed. "
            "Please check that the file contains readable "
            "financial information."
        )

    # Empty / unreadable input
    if any(
        keyword in message
        for keyword in [
            "empty",
            "no usable data",
            "unable to read",
        ]
    ):
        return (
            400,
            "The uploaded document is empty or could not be read."
        )

    # File not found
    if "file not found" in message:
        return (
            404,
            "The uploaded document could not be found."
        )

    # Everything else
    return (
        500,
        "We couldn't generate the financial report. "
        "Please try again."
    )


@router.post("/upload")
async def upload_document(
    company_name: str = Form(...),
    file: UploadFile = File(...)
):

    # ---------------------------------------------------------
    # VALIDATE COMPANY NAME
    # ---------------------------------------------------------

    company_name = company_name.strip()

    if not company_name:
        raise HTTPException(
            status_code=400,
            detail="Please enter a company name."
        )

    # ---------------------------------------------------------
    # VALIDATE FILE
    # ---------------------------------------------------------

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Please select a file."
        )

    extension = os.path.splitext(
        file.filename
    )[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. "
                   "Please upload a PDF, CSV, or TXT file."
        )

    file_bytes = await file.read()

    if not file_bytes:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty."
        )

    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File size must be less than 50 MB."
        )

    # ---------------------------------------------------------
    # SAVE SOURCE FILE
    # ---------------------------------------------------------

    file_id = str(uuid.uuid4())

    input_filename = (
        f"{file_id}{extension}"
    )

    input_path = os.path.join(
        UPLOAD_DIR,
        input_filename
    )

    with open(
        input_path,
        "wb"
    ) as output_file:
        output_file.write(file_bytes)

    # ---------------------------------------------------------
    # PROCESS DOCUMENT
    # ---------------------------------------------------------

    try:

        # 1. Gemini extraction
        gemini_service = GeminiService()

        extracted_data = (
            gemini_service.extract_financial_data(
                input_path,
                company_name
            )
        )

        # 2. Gemini → internal report model
        financial_report = (
            map_gemini_to_financial_report(
                extracted_data
            )
        )

        if financial_report is None:
            raise ValueError(
                "Financial report mapping returned no data."
            )

        # Ensure entered company name is retained.
        if financial_report.company:
            financial_report.company.name = (
                company_name
            )

        # 3. Safe report filename
        safe_company_name = "".join(
            character
            if character.isalnum()
            or character in (" ", "_", "-")
            else "_"
            for character in company_name
        ).strip()

        report_filename = (
            f"{safe_company_name}_"
            f"{file_id[:8]}_"
            f"financial_report.pdf"
        )

        report_path = os.path.join(
            REPORT_DIR,
            report_filename
        )

        # 4. Generate PDF
        FinancialReportPDF(
            financial_report,
            report_path
        ).build()

        # Verify that PDF actually exists.
        if not os.path.isfile(report_path):
            raise RuntimeError(
                "PDF generation completed but the "
                "report file was not created."
            )

        return {
            "success": True,
            "message": (
                "Financial report generated successfully."
            ),
            "company_name": company_name,
            "report": {
                "filename": report_filename,
                "download_url": (
                    f"/api/reports/{report_filename}"
                ),
            },
        }

    except HTTPException:
        raise

    except Exception as exc:

        status_code, user_message = (
            friendly_error(exc)
        )

        print(
            f"[REPORT ERROR] "
            f"{type(exc).__name__}: {exc}"
        )

        raise HTTPException(
            status_code=status_code,
            detail=user_message
        )


# -------------------------------------------------------------
# PDF DOWNLOAD
# -------------------------------------------------------------

@router.get("/reports/{filename}")
async def download_report(
    filename: str
):

    # Prevent path traversal.
    safe_filename = os.path.basename(
        filename
    )

    report_path = os.path.join(
        REPORT_DIR,
        safe_filename
    )

    if not os.path.isfile(report_path):
        raise HTTPException(
            status_code=404,
            detail="Report not found."
        )

    return FileResponse(
        report_path,
        media_type="application/pdf",
        filename=safe_filename
    )