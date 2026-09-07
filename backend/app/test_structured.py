from google import genai
from google.genai import types

from app.config import settings
from app.models.test_schema import TestFinancialData


client = genai.Client(
    api_key=settings.gemini_api_key
)


response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="""
    Return the following financial information as structured data:

    Company: Eternal Limited
    Rating: HOLD
    Target Price: 337
    Current Price: 306
    """,
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=TestFinancialData,
    )
)


print("=" * 80)
print("STRUCTURED OUTPUT TEST")
print("=" * 80)

print(response.text)

print("=" * 80)

result = TestFinancialData.model_validate_json(
    response.text
)

print(result)

print("=" * 80)