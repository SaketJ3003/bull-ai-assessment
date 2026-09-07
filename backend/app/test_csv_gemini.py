from app.services.gemini_service import GeminiService
from app.services.mapper import map_gemini_to_financial_report


CSV_PATH = "sample_data/test_financials.csv"


def main():
    print("=" * 80)
    print("STEP 1: CSV → GEMINI")
    print("=" * 80)

    service = GeminiService()

    extracted = service.extract_financial_data(
        CSV_PATH,
        "Test Company"
    )

    print("\nGemini extraction successful.")

    print("\nCompany:")
    print(extracted.company)

    print("\nAnnual financials:")

    for item in extracted.annual_financials:
        print(item)

    print("\n" + "=" * 80)
    print("STEP 2: GEMINI → MAPPER")
    print("=" * 80)

    report = map_gemini_to_financial_report(
        extracted
    )

    print("\nMapper successful.")

    print("\nMapped company:")
    print(report.company)

    print("\nMapped annual financials:")

    for item in report.annual_financials:
        print(item)

    print("\n" + "=" * 80)
    print("CSV → GEMINI → MAPPER SUCCESS")
    print("=" * 80)


if __name__ == "__main__":
    main()