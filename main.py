from fastapi import FastAPI
from pydantic import BaseModel
import os, json, traceback
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()                      # ← CRÉÉ AVANT TOUTES LES ROUTES

@app.get("/")
def ping():
    return {"ok": True}

# --------- Models ---------
class Brief(BaseModel):
    activity: str
    goal: str
    colors: str
    inspiration: str

class Section(BaseModel):
    id: str
    title: str
    copy_text: str          # ← évite le nom 'copy' (warning Pydantic)
    img_prompt: str

class Spec(BaseModel):
    sections: list[Section]

PROMPT_BASE = """... ton prompt ..."""

@app.post("/spec")
def make_spec(data: Brief):
    try:
        prompt = PROMPT_BASE.format(**data.dict())
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        ).choices[0].message.content

        parsed = json.loads(resp)
        spec = Spec(**parsed)
        return spec.dict()

    except Exception as e:
        return {"error": str(e), "trace": traceback.format_exc()}
