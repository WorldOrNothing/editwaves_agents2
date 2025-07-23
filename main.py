import os, json
from fastapi import FastAPI
from pydantic import BaseModel
from schema import Spec
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
app = FastAPI()

class Brief(BaseModel):
    activity: str
    goal: str
    colors: str
    inspiration: str

PROMPT_BASE = """Tu es expert en landing pages.
Renvoie UNIQUEMENT un JSON valide:
{
  "sections": [
    {"id":"hero","title":"...","copy":"...","img_prompt":"..."}
  ]
}
Règles:
- 3 à 8 sections
- Français clair (niveau B2)
- CTA = verbe d’action
- img_prompt = prompt image sans texte (style flat/illustration)

Données:
Activité: {activity}
Objectif: {goal}
Couleurs: {colors}
Inspiration: {inspiration}
"""

@app.post("/spec")
def make_spec(data: Brief):
    prompt = PROMPT_BASE.format(**data.dict())
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        temperature=0.4
    ).choices[0].message.content

    parsed = json.loads(resp)          # peut lever une erreur -> try/except plus tard
    spec = Spec(**parsed)              # validation Pydantic
    return spec.dict()
