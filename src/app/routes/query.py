from fastapi import APIRouter
from pydantic import BaseModel
from utils.llms.llm_router import query_with_personas

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

@router.post("/")
async def query_endpoint(req: QueryRequest):
    """Receives a user question and queries 20 personas via LLM."""
    results = await query_with_personas(req.question)
    return {"question": req.question, "results": results}
