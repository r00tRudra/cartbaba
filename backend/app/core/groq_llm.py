from groq import Groq
from app.core.config import settings

client = Groq(api_key=settings.GROQ_API_KEY)

def call_llm(prompt, model="groq/gpt-oss-20b"):
    response = client.chat.completions.create(
        model=model,   # ⚠️ no "groq/" here
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content
