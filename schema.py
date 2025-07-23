from pydantic import BaseModel
from typing import List

class Section(BaseModel):
    id: str
    title: str
    copy: str
    img_prompt: str

class Spec(BaseModel):
    sections: List[Section]
