import json
from pydantic import BaseModel
import openai

class Section(BaseModel):
    id: str
    title: str
    copy: str
    img_prompt: str

class Spec(BaseModel):
    sections: list[Section]

PROMPT_BASE = """Tu es expert en landing pages...
Renvoie UNIQUEMENT un JSON valide:
{
  "sections":[
    {"id":"hero","title":"...","copy":"...","img_prompt":"..."}
  ]
}
Règles:
- 3 à 8 sections
- Français clair
- CTA = verbe d’action
- img_prompt = prompt image (pas de texte)

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

    try:
        parsed = json.loads(resp)
        spec = Spec(**parsed)       # valid pydantic
        return spec.dict()
    except Exception as e:
        return {"error":"json_parse_failed", "raw": resp, "msg": str(e)}
