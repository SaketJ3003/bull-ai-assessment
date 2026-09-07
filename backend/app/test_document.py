from app.services.gemini_service import analyze_document


file_path = "generated/uploads/e6d2265d-1ef2-4699-aa0d-f5512fc87091.pdf"


result = analyze_document(file_path)


print("\n")
print("=" * 80)
print("STRUCTURED FINANCIAL ANALYSIS")
print("=" * 80)

print(
    result.model_dump_json(
        indent=2
    )
)

print("=" * 80)