from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .chatbot import hybrid_chatbot
import os

app = FastAPI(title="AUPP FAQ Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    query: str


@app.post("/chat")
def chat(request: Query):
    result = hybrid_chatbot(request.query)
    return {
        "query": request.query,
        "category": result["category"],
        "similarity": result["similarity"],
        "answer": result["answer"]
    }

frontend_path = os.path.join(os.path.dirname(__file__), "../frontend/index.html")

@app.get("/")
def root():
    return FileResponse(frontend_path)
