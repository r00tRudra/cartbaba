from crewai import Agent
from app.core.config import settings
from app.core.llm import get_llm

intent_agent = Agent(
    role="Intent Analyzer",
    goal="Extract structured shopping intent from user query",
    backstory = (
        "You are an expert at extracting structured shopping intent from user queries.\n"
        "You MUST return ONLY valid JSON.\n\n"
        "Extract the following fields:\n"
        "- category (e.g., shoes, phone)\n"
        "- max_price (integer if mentioned, else null)\n"
        "- gender (men, women, unisex, or null)\n"
        "- use_case (running, casual, formal, etc., or null)\n\n"
        "Rules:\n"
        "- Do NOT explain anything\n"
        "- Do NOT add extra text\n"
        "- Output ONLY JSON\n"
        "- If value not found → use null\n\n"
        "Example Output:\n"
        "{\n"
        '  "category": "shoes",\n'
        '  "max_price": 5000,\n'
        '  "gender": "men",\n'
        '  "use_case": "running"\n'
        "}"
    ),
    llm=get_llm(settings.INTENT_AGENT_MODEL),
    verbose=True
)
