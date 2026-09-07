from app.services.gemini_service import GeminiService
from app.services.mapper import map_gemini_to_financial_report


PDF_PATH = "generated/uploads/e6d2265d-1ef2-4699-aa0d-f5512fc87091.pdf"


def main():

    print("=" * 80)
    print("STEP 1: GEMINI EXTRACTION")
    print("=" * 80)

    gemini_service = GeminiService()

    extracted = gemini_service.extract_financial_data(
        PDF_PATH
    )

    print("Gemini extraction successful.")

    print("\n" + "=" * 80)
    print("STEP 2: MAPPING TO FINANCIAL REPORT")
    print("=" * 80)

    report = map_gemini_to_financial_report(
        extracted
    )

    print("Mapping successful.")

    print("\n" + "=" * 80)
    print("FINAL FINANCIAL REPORT")
    print("=" * 80)

    print("\nCompany:")
    print(report.company)

    print("\nRecommendation:")
    print(report.recommendation)

    print("\nCompany Data:")
    print(report.company_data)

    print("\nAnnual Financials:")

    for item in report.annual_financials:
        print(item)

    print("\nQuarterly Financials:")

    for item in report.quarterly_financials:
        print(item)

    print("\nKey Highlights:")

    for item in report.key_highlights:
        print("-", item)

    print("\n" + "=" * 80)
    print("MAPPER TEST SUCCESSFUL")
    print("=" * 80)


if __name__ == "__main__":
    main()