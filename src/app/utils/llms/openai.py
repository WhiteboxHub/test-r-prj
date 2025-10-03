import os
import openai
from typing import List

class OpenAIClient:
    def __init__(self, model: str = None):
        api_key = os.getenv("OPENAI_API_KEY","KEY HERE")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set in environment.")
        openai.api_key = api_key
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    async def chat(self, prompt: str) -> str:
        resp = await openai.ChatCompletion.acreate(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=512,
        )
        return resp.choices[0].message["content"].strip()