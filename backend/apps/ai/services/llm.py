from google import genai
from django.conf import settings


client = genai.Client(api_key=settings.API_KEY)

def call_llm(system_prompt, user_prompt):
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=user_prompt,
        config={
            "system_instruction": system_prompt,
        },
    )
    return response.text
