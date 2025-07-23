from fastapi import FastAPI
import os, json
from pydantic import BaseModel
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

@app.get("/")
def ping():
    return {"ok": True}

class Brief(BaseModel):
    activity: str
    goal: str
    colors: str
    inspiration: str

@app.post("/spec")
def make_spec(data: Brief):
    # Pour l’instant renvoie juste ce que tu reçois (on branchera OpenAI après)
    return {"received": data.dict()}
