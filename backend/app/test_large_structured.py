from google import genai
from google.genai import types

from app.config import settings
from app.models.gemini_schema import GeminiFinancialExtraction


client = genai.Client(api_key=settings.gemini_api_key)


prompt = """
Extract the following financial information into structured data.

Company:
Eternal Limited

Sector:
Internet & Catalogue Retail

Rating:
HOLD

Target Price:
337

Current Price:
306

Expected Return:
10%

Market Cap:
295735

52 Week High:
314

52 Week Low:
190

Enterprise Value:
294166

Outstanding Shares:
965

Free Float:
71.9%

Beta:
1.0

Face Value:
1.0

Annual Financials:

FY25A:
Sales 20243
Sales Growth 67.1
EBITDA 637
EBITDA Margin 3.1
Adjusted PAT 527
PAT Growth 50.1
Adjusted EPS 0.6
EPS Growth 46.3

FY26E:
Sales 35020
Sales Growth 73.0
EBITDA 1248
EBITDA Margin 3.6
Adjusted PAT 927
PAT Growth 75.9
Adjusted EPS 1.0
EPS Growth 60.1

FY27E:
Sales 54632
Sales Growth 56.0
EBITDA 3575
EBITDA Margin 6.5
Adjusted PAT 2643
PAT Growth 185.2
Adjusted EPS 2.7
EPS Growth 185.2

Key Highlights:
- Food delivery NOV growth was 13% YoY.
- Blinkit NOV grew strongly.
- Blinkit achieved profitability in some cities.
- Quick commerce is transitioning toward inventory ownership.
"""


response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=prompt,
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=GeminiFinancialExtraction,
    ),
)


print("=" * 80)
print("LARGE STRUCTURED OUTPUT TEST")
print("=" * 80)

print(response.text)

print("=" * 80)
print("VALIDATED PYDANTIC OBJECT")
print("=" * 80)

result = GeminiFinancialExtraction.model_validate_json(response.text)

print(result)

print("=" * 80)
print("COMPANY:", result.company.name)
print("RATING:", result.recommendation.rating)
print("TARGET:", result.recommendation.target_price)
print("ANNUAL RECORDS:", len(result.annual_financials))
print("HIGHLIGHTS:", len(result.key_highlights))
print("=" * 80)