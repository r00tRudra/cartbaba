
from crewai import Agent
from app.core.config import settings
from app.core.llm import get_llm

final_agent = Agent(
    role="CartBaba Assistant",
    goal="Generate user-friendly shopping recommendations",
    backstory = (
        "You are a helpful shopping assistant.\n\n"
        "You receive a list of ranked products.\n"
        "Explain recommendations clearly.\n\n"
        "Rules:\n"
        "- Be concise\n"
        "- Highlight why each product is good\n"
        "- Do NOT invent data\n"
        "- Keep it user-friendly\n\n"
        "Format:\n"
        "Top recommendations with short explanations"
    ),
    llm=get_llm(settings.FINAL_AGENT_MODEL),
    verbose=True
)
