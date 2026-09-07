import os

from pypdf import PdfReader

from app.services.gemini_service import GeminiService
from app.services.mapper import map_gemini_to_financial_report
from app.pdf.generator import FinancialReportPDF


CSV_PATH = "sample_data/test_financials.csv"
OUTPUT_PATH = "generated/test_csv_financial_report.pdf"


def main():

    print("=" * 80)
    print("STEP 1: CSV → GEMINI")
    print("=" * 80)

    service = GeminiService()

    extracted = service.extract_financial_data(
        CSV_PATH,
        "Test Company"
    )

    print("Gemini extraction successful.")

    print("\nAnnual financials:")
    for item in extracted.annual_financials:
        print(item)

    print("\n" + "=" * 80)
    print("STEP 2: GEMINI → FINANCIAL REPORT")
    print("=" * 80)

    report = map_gemini_to_financial_report(
        extracted
    )

    print("Mapper successful.")

    print("\nCompany:")
    print(report.company)

    print("\n" + "=" * 80)
    print("STEP 3: FINANCIAL REPORT → PDF")
    print("=" * 80)

    os.makedirs(
        os.path.dirname(OUTPUT_PATH),
        exist_ok=True
    )

    FinancialReportPDF(
        report,
        OUTPUT_PATH
    ).build()

    print("\nPDF generated successfully.")

    print("\n" + "=" * 80)
    print("STEP 4: PDF VALIDATION")
    print("=" * 80)

    reader = PdfReader(OUTPUT_PATH)

    page_count = len(reader.pages)

    print(f"PDF path: {OUTPUT_PATH}")
    print(f"Pages: {page_count}")

    if page_count != 4:
        raise RuntimeError(
            f"Expected 4 pages, but generated {page_count} pages."
        )

    print("\n" + "=" * 80)
    print("CSV → GEMINI → MAPPER → PDF SUCCESS")
    print("=" * 80)


if __name__ == "__main__":
    main()