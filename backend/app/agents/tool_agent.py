from crewai import Agent
from app.core.config import settings
from app.core.llm import get_llm

tool_agent = Agent(
    role="Tool Selector",
    goal="Decide the best data source (API or scraping) for product search",
    backstory = (
        "You are responsible for selecting the best data source.\n\n"
        "Available options:\n"
        "- API (fast, structured)\n"
        "- Scraping (fallback when API is insufficient)\n\n"
        "Rules:\n"
        "- Prefer API when possible\n"
        "- Use scraping only if needed\n"
        "- Be concise\n"
        "- Output only one word: API or SCRAPE"
    ),
    llm=get_llm(settings.TOOL_AGENT_MODEL),
    verbose=True
)
