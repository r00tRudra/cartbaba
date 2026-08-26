from crewai import LLM




def get_llm(model: str | None = "groq/gpt-oss-20b"):
    return LLM(
        model=model,
        temperature=0.2,
        additional_drop_params=["cache_control", "cache_breakpoint"],
    )
