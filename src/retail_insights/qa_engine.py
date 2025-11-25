from .agents import LanguageResolutionAgent, DataExtractionAgent, ValidationAgent
from .llm_client import LLMClient


class QAEngine:
    def __init__(self, data_layer):
        self.lang_agent = LanguageResolutionAgent()
        self.data_agent = DataExtractionAgent(data_layer)
        self.validate_agent = ValidationAgent()
        self.llm = LLMClient()

    def ask(self, question: str) -> str:
        plan = self.lang_agent.resolve(question)
        extraction = self.data_agent.extract(plan)
        validation = self.validate_agent.validate(extraction)
        if not validation.get('ok'):
            return "Validation error: " + ", ".join(validation.get('errors', []))

        # Build a context string to feed to the LLM
        context_parts = []
        for k, v in extraction.items():
            try:
                context_parts.append(f"{k}:\n{v.to_string(index=False, max_rows=10)}")
            except Exception:
                context_parts.append(f"{k}: {str(v)[:400]}")

        prompt = "You are a retail insights assistant. Answer the question below using the context."
        prompt += "\nCONTEXT:\n" + "\n---\n".join(context_parts) + f"\nQUESTION: {question}\nAnswer concisely."

        return self.llm.generate(prompt)
