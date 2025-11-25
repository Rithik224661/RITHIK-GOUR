import os
from typing import Optional
import openai

class LLMClient:
    """Lightweight LLM client wrapper supporting OpenAI and a local fallback.

    If OPENAI_API_KEY or GEMINI_API_KEY is present in env, it will use OpenAI API.
    Otherwise it provides a simple deterministic, rule-based fallback used for offline demo/tests.
    """

    def __init__(self):
        self.openai_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("GEMINI_API_KEY")
        if self.openai_key:
            openai.api_key = self.openai_key

    def generate(self, prompt: str, max_tokens: int = 256, temperature: float = 0.2) -> str:
        if self.openai_key:
            resp = openai.ChatCompletion.create(
                model="gpt-4o-mini" if True else "gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            # handle variations in response structure
            content = None
            try:
                content = resp.choices[0].message.content
            except Exception:
                content = str(resp)
            return content

        # Fallback: simple echo + short canned processing
        # Keep it deterministic and safe for offline demo.
        if "summarize" in prompt.lower():
            return "(Offline) Summary: Sales grew 2.5% YoY; top region: West; top product: Widgets."
        if "which product" in prompt.lower() or "underperform" in prompt.lower():
            return "(Offline) Q&A: Product line 'Accessories' underperformed in Q4 compared to previous quarters."
        return "(Offline) I am running in local fallback mode. Provide an API key (OPENAI_API_KEY or GEMINI_API_KEY) to enable LLM-powered outputs."
