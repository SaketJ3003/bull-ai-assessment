from app.services.gemini_service import GeminiService


PDF_PATH = "generated/uploads/e6d2265d-1ef2-4699-aa0d-f5512fc87091.pdf"


def main():

    service = GeminiService()

    result = service.extract_financial_data(PDF_PATH)

    print("\n" + "=" * 80)
    print("REAL DOCUMENT EXTRACTION")
    print("=" * 80)

    print("\nCOMPANY")
    print(result.company)

    print("\nRECOMMENDATION")
    print(result.recommendation)

    print("\nCOMPANY DATA")
    print(result.company_data)

    print("\nANNUAL FINANCIALS")
    for item in result.annual_financials:
        print(item)

    print("\nQUARTERLY FINANCIALS")
    for item in result.quarterly_financials:
        print(item)

    print("\nKEY HIGHLIGHTS")
    for item in result.key_highlights:
        print("-", item)

    print("\nRISKS")
    for item in result.risks:
        print("-", item)

    print("\nESTIMATE CHANGES")
    for item in result.estimate_changes:
        print(item)

    print("\nPROFIT & LOSS")
    for item in result.profit_loss:
        print(item)

    print("\nBALANCE SHEET")
    for item in result.balance_sheet:
        print(item)

    print("\nCASH FLOW")
    for item in result.cash_flow:
        print(item)

    print("\nRATIOS")
    for item in result.ratios:
        print(item)

    print("\nRECOMMENDATION HISTORY")
    for item in result.recommendation_history:
        print(item)

    print("\nCHARTS")
    for item in result.charts:
        print(item)

    print("\n" + "=" * 80)
    print("EXTRACTION COMPLETED SUCCESSFULLY")
    print("=" * 80)


if __name__ == "__main__":
    main()