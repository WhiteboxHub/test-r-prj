import asyncio
from pathlib import Path
import json

# from persona_generator.persona_generator import PersonaGenerator
from utils.llms.openai import OpenAIClient
from utils.prompts.prompt_templates import persona_prompt

# Paths
BASE_DIR = Path(__file__).resolve().parents[3]  # points to src/
DATA_DIR = BASE_DIR / "data"
PERSONAS_FILE = DATA_DIR / "personas.json"
DISTRIBUTION_FILE = BASE_DIR / "distributions_extractor" / "sample_distributions.json"

# Ensure data directory exists
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Load or generate personas
# if not PERSONAS_FILE.exists():
#     print("⚠️ personas.json not found. Generating now...")
#     generator = PersonaGenerator(DISTRIBUTION_FILE)
#     generator.save_personas(PERSONAS_FILE, n=20)
#     print(f"✅ Generated personas.json at {PERSONAS_FILE}")

with open(PERSONAS_FILE, "r") as f:
    PERSONAS = json.load(f)

if not PERSONAS:
    raise ValueError("No personas found in personas.json after generation!")

# Async query function
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

    # Run all queries concurrently
    responses = await asyncio.gather(*tasks)

    # Map responses back to persona IDs
    results = [
        {"persona_id": p["persona_id"], "response": r}
        for p, r in zip(PERSONAS, responses)
    ]
    return results
