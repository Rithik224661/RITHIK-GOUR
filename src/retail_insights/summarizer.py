from .agents import LanguageResolutionAgent, DataExtractionAgent, ValidationAgent
from .llm_client import LLMClient


class Summarizer:
    def __init__(self, data_layer):
        self.llm = LLMClient()
        self.lang_agent = LanguageResolutionAgent()
        self.data_agent = DataExtractionAgent(data_layer)
        self.validate_agent = ValidationAgent()

    def summarize(self, prompt: str = "Summarize performance") -> str:
        plan = self.lang_agent.resolve(prompt)
        extraction = self.data_agent.extract(plan)
        validation = self.validate_agent.validate(extraction)
        if not validation.get('ok'):
            return "Data validation failed: " + ", ".join(validation.get('errors', []))

        # Create a short text summary using LLM (or fallback)
        text_for_llm = "Summarize the following analytics result for product sales: " + str({k: v.head(5).to_dict() for k, v in extraction.items() if hasattr(v, 'head')})
        return self.llm.generate(text_for_llm)
