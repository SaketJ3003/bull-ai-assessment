from google import genai

from app.config import settings


client = genai.Client(
    api_key=settings.gemini_api_key
)


response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Explain EBITDA in one sentence."
)


print(response.text)