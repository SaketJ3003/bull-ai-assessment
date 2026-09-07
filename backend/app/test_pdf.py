import os

from app.services.gemini_service import GeminiService
from app.services.mapper import map_gemini_to_financial_report
from app.pdf.generator import FinancialReportPDF


PDF_PATH = "generated/uploads/e6d2265d-1ef2-4699-aa0d-f5512fc87091.pdf"

OUTPUT_PATH = "generated/financial_report_test.pdf"


def main():

    print("=" * 80)
    print("STEP 1: EXTRACT")
    print("=" * 80)

    gemini_service = GeminiService()

    extracted = gemini_service.extract_financial_data(
        PDF_PATH
    )

    print("Extraction successful.")

    print("=" * 80)
    print("STEP 2: MAP")
    print("=" * 80)

    report = map_gemini_to_financial_report(
        extracted
    )

    print("Mapping successful.")

    print("=" * 80)
    print("STEP 3: GENERATE PDF")
    print("=" * 80)

    os.makedirs(
        "generated",
        exist_ok=True,
    )

    generator = FinancialReportPDF(
        report=report,
        output_path=OUTPUT_PATH,
    )

    output = generator.build()

    print("=" * 80)
    print("PDF GENERATED SUCCESSFULLY")
    print("=" * 80)

    print(f"File: {output}")


if __name__ == "__main__":
    main()