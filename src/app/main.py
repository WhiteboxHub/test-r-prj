import json
from pathlib import Path
from fastapi import FastAPI
import uvicorn

from routes import query
from utils.llms.llm_router import query_with_personas

app = FastAPI(title="Pulmonologist Persona QA App")

# include routes
app.include_router(query.router, prefix="/api/v1/query", tags=["Query"])

@app.get("/")
async def root():
    return {"message": "Pulmonologist Persona QA App is running!"}

@app.on_event("startup")
async def run_batch_on_startup():
    """
    On startup, read questions.json from data folder,
    query all personas, and write results to output.json.
    """
    data_dir = Path(__file__).resolve().parents[1] / "data"
    questions_file = data_dir / "questions.json"
    output_file = data_dir / "output.json"

    if not questions_file.exists():
        print(f"⚠️ No questions.json found at {questions_file}")
        return

    questions = json.loads(questions_file.read_text())

    all_results = []
    for q in questions:
        q_text = q["text"]
        results = await query_with_personas(q_text)
        all_results.append({
            "id": q["id"],
            "question": q_text,
            "results": results
        })

    output_file.write_text(json.dumps(all_results, indent=2))
    print(f"✅ Wrote results for {len(questions)} questions to {output_file}")


# 👇 this makes it runnable via `python main.py`
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)