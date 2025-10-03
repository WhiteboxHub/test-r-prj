import torch
from bert_score import score
from utils.llms.openai import OpenAIClient

async def judge_with_openai(persona: dict, response: str) -> str:
    """Ask OpenAI if the response reflects persona traits."""
    judge_prompt = f"""
You are evaluating a simulated pulmonologist response.

Persona: {persona}
Response: {response}

Does the response clearly reflect this persona's background and likely practice style?
Answer with Yes/No and give a short justification.
"""
    client = OpenAIClient(model="gpt-4o-mini")
    return await client.chat(judge_prompt)


def check_relevancy_with_bertscore(reference: str, candidate: str, lang: str = "en"):
    """Use BERTScore to measure semantic similarity."""
    P, R, F1 = score([candidate], [reference], lang=lang)
    return {"precision": float(P.mean()), "recall": float(R.mean()), "f1": float(F1.mean())}