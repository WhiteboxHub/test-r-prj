import asyncio
from pathlib import Path
import json

from utils.llms.openai import OpenAIClient
from utils.prompts.prompt_templates import persona_prompt


BASE_DIR = Path(__file__).resolve().parents[3] 
DATA_DIR = BASE_DIR / "data"
PERSONAS_FILE = DATA_DIR / "personas.json"
DISTRIBUTION_FILE = BASE_DIR / "distributions_extractor" / "sample_distributions.json"


DATA_DIR.mkdir(parents=True, exist_ok=True)


with open(PERSONAS_FILE, "r") as f:
    PERSONAS = json.load(f)

if not PERSONAS:
    raise ValueError("No personas found in personas.json after generation!")


async def query_with_personas(question: str):
    """
    Send the same question through all personas using the LLM.
    Returns a list of responses, one per persona.
    """
    client = OpenAIClient()
    tasks = []

    for persona in PERSONAS:
        prompt = persona_prompt(persona, question)
        tasks.append(client.chat(prompt))

 
    responses = await asyncio.gather(*tasks)

  
    results = [
        {"persona_id": p["persona_id"], "response": r}
        for p, r in zip(PERSONAS, responses)
    ]
    return results
