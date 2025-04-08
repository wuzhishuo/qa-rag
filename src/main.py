from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from .app.rag_chain import get_qa_chain
import asyncio


web_app = FastAPI()
qa_chain = get_qa_chain(logging=False)

class QARequest(BaseModel):
    query: str
    history: list = []

@web_app.post("/qa")
def answer_question(req: QARequest):
    try:
        result = qa_chain.invoke({"query": req.query, "history": req.history})
        return {"answer": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@web_app.post("/qa/stream")
async def answer_question_stream(req: QARequest):
    try:
        async def generate():
            for chunk in qa_chain.stream({"query": req.query, "history": req.history}):
                yield chunk + "\n"
        return StreamingResponse(generate(), media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))