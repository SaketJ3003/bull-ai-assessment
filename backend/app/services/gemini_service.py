import os
import time

from dotenv import load_dotenv

load_dotenv()

from google import genai
from google.genai import types

from app.models.gemini_schema import GeminiFinancialExtraction
from app.parsers.csv_parser import parse_csv
from app.parsers.txt_parser import parse_txt

class GeminiService:

    MODEL_NAME = "gemini-3.6-flash"

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is not configured."
            )

        self.client = genai.Client(
            api_key=api_key
        )

    def _generate_with_retry(self, contents, config):
        """
        Generate Gemini response with retry handling for
        temporary API availability/rate-limit errors.
        """

        max_attempts = 4
        base_delay = 2

        for attempt in range(max_attempts):

            try:
                return self.client.models.generate_content(
                    model=self.MODEL_NAME,
                    contents=contents,
                    config=config,
                )

            except Exception as exc:

                error_text = str(exc)

                retryable = any(
                    code in error_text
                    for code in [
                        "429",
                        "500",
                        "502",
                        "503",
                        "504",
                        "UNAVAILABLE",
                        "RESOURCE_EXHAUSTED",
                    ]
                )

                if not retryable or attempt == max_attempts - 1:
                    raise

                delay = base_delay * (2 ** attempt)

                print(
                    f"Gemini temporary error. "
                    f"Retrying in {delay}s..."
                )

                time.sleep(delay)

    def _build_prompt(self, company_name: str) -> str:

        return f"""
You are a financial research data extraction assistant.

The user supplied financial information for:

Company name: {company_name}

Extract ONLY information supported by the supplied document.

Return structured financial research data that can populate
a Geojit-style equity research report.

Extract, whenever available:

1. Company information
2. Recommendation
3. Company data
4. Shareholding
5. Price performance
6. Annual financial summary
7. Quarterly financials
8. Outlook and valuation
9. Business summary
10. Key highlights
11. Risks
12. Estimate changes
13. Profit and Loss
14. Balance Sheet
15. Cash Flow
16. Financial ratios
17. Chart data
18. Recommendation history

IMPORTANT RULES:

- Do NOT invent financial values.
- Do NOT calculate values unless the source explicitly provides
  enough information and the calculation is clearly required.
- If a field is unavailable, return null, an empty list, or the
  appropriate empty value allowed by the schema.
- Preserve the units used by the source where possible.
- Preserve historical and estimated periods such as FY25A, FY26E,
  FY27E, Q1FY26, etc.
- Distinguish actual values from estimates.
- Preserve percentages and growth rates when explicitly provided.
- Extract narrative information for outlook, business summary,
  highlights, and risks.
- If chart values are available in tabular form, extract them.
- Do not infer chart values from visual appearance.
- The entered company name should be represented as the company
  name unless the document clearly provides a different official
  name.

The output must conform exactly to the supplied structured schema.
"""

    def extract_financial_data(
        self,
        file_path: str,
        company_name: str = ""
    ) -> GeminiFinancialExtraction:

        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        extension = os.path.splitext(
            file_path
        )[1].lower()

        prompt = self._build_prompt(
            company_name or "Unknown Company"
        )

        config = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=GeminiFinancialExtraction,
        )

        # ---------------------------------------------------------
        # PDF
        # ---------------------------------------------------------
        if extension == ".pdf":

            uploaded_file = self.client.files.upload(
                file=file_path
            )

            contents = [
                uploaded_file,
                prompt,
            ]

        # ---------------------------------------------------------
        # CSV
        # ---------------------------------------------------------
        elif extension == ".csv":

            csv_text = parse_csv(file_path)

            contents = [
                prompt,
                "\n\nSOURCE DOCUMENT TYPE: CSV\n\n",
                csv_text,
            ]

        # ---------------------------------------------------------
        # TXT
        # ---------------------------------------------------------
        elif extension == ".txt":

            txt_text = parse_txt(file_path)

            contents = [
                prompt,
                "\n\nSOURCE DOCUMENT TYPE: TXT\n\n",
                txt_text,
            ]

        else:

            raise ValueError(
                f"Unsupported file type: {extension}"
            )

        response = self._generate_with_retry(
            contents=contents,
            config=config,
        )

        if not response or not response.text:
            raise ValueError(
                "Gemini returned an empty response."
            )

        try:
            return GeminiFinancialExtraction.model_validate_json(
                response.text
            )

        except Exception as exc:
            raise ValueError(
                f"Unable to parse Gemini structured response: {exc}"
            ) from exc