import asyncio
from pathlib import Path
import json

from utils.llms.openai import OpenAIClient
from utils.prompts.prompt_templates import persona_prompt

# load generated personas
PERSONAS_FILE = Path(__file__).resolve().parents[3] / "personas.json"
if PERSONAS_FILE.exists():
    PERSONAS = json.loads(PERSONAS_FILE.read_text())
else:
    PERSONAS = []

async def query_with_personas(question: str):
    """Send the same question through 20 personas using LLM."""
    if not PERSONAS:
        raise ValueError("No personas found. Please generate personas.json first.")

    client = OpenAIClient()
    tasks = []
    for persona in PERSONAS:
        print(persona,question)
        prompt = persona_prompt(persona, question)
        tasks.append(client.chat(prompt))

    responses = await asyncio.gather(*tasks)
    results = [
        {"persona_id": p["id"], "response": r}
        for p, r in zip(PERSONAS, responses)
    ]
    return results