from crewai import Agent
from app.core.config import settings
from app.core.llm import get_llm

review_agent = Agent(
    role="Product Reviewer",
    goal="Filter out irrelevant or low-quality products",
    backstory = (
        "You filter and clean product lists based on user intent.\n\n"
        "Rules:\n"
        "- Remove irrelevant products\n"
        "- Remove overpriced items\n"
        "- Remove low-quality items (rating < 3.5 if available)\n"
        "- Keep only best matches\n\n"
        "Return ONLY filtered JSON list.\n"
        "No explanation."
    ),
    llm=get_llm(settings.REVIEW_AGENT_MODEL),
    verbose=True
)
