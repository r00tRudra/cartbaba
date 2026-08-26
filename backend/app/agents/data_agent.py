from crewai import Agent
from app.core.config import settings
from app.core.llm import get_llm

data_agent = Agent(
    role="Data Extractor",
    goal="Fetch relevant product data from available sources",
    backstory = (
        "You process raw product data and convert it into structured format.\n\n"
        "Each product must contain:\n"
        "- name\n"
        "- price\n"
        "- rating\n"
        "- source\n\n"
        "Rules:\n"
        "- Return ONLY a JSON list\n"
        "- No explanation\n"
        "- Remove incomplete items\n"
    ),
    llm=get_llm(settings.DATA_AGENT_MODEL),
    verbose=True
)
