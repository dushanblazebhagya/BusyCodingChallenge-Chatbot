from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from server import query_resume_tool, send_email_tool

app = FastAPI()

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/query_resume")
async def query_resume_endpoint(payload: dict):
    question = payload.get("question", "")
    loop = asyncio.get_event_loop()
    try:
        answer = await loop.run_in_executor(None, lambda: query_resume_tool(question))
        return {"answer": answer}
    except Exception as e:
        return {"error": str(e)}

@app.post("/send_email")
async def send_email_endpoint(payload: dict):
    recipient = payload.get("recipient", "")
    subject = payload.get("subject", "")
    body = payload.get("body", "")
    loop = asyncio.get_event_loop()
    try:
        answer = await loop.run_in_executor(None, lambda: send_email_tool(recipient, subject, body))
        return {"message": answer}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
