from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from utils.llms.llm_router import query_with_personas
from evals.llm_as_a_judge import judge_with_openai, check_relevancy_with_bertscore

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

@router.post("/")
async def query_endpoint(req: QueryRequest):
    """
    Receives a user question, queries personas,
    then evaluates each response with LLM as Judge + BERTScore.
    """
    results: List[Dict] = await query_with_personas(req.question)

    approved_results = []

    for persona_result in results:
        persona = persona_result.get("persona")
        response = persona_result.get("response")

        verdict = await judge_with_openai(persona, response)

        if "yes" not in verdict.lower(): 
            continue

        relevancy = check_relevancy_with_bertscore(req.question, response)

        if relevancy["f1"] < 0.7: 
            continue

    
        persona_result["judge_verdict"] = verdict
        persona_result["relevancy_score"] = relevancy

        approved_results.append(persona_result)

  
    if not approved_results:
        raise HTTPException(status_code=400, detail="No persona responses passed Judge evaluation")

    return {
        "question": req.question,
        "approved_count": len(approved_results),
        "total_checked": len(results),
        "results": approved_results,
    }
