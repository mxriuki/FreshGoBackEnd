from fastapi import FastAPI, HTTPException # type: ignore
from pydantic import BaseModel # type: ignore
from typing import List, Optional
from uuid import UUID, uuid4

class Recipe(BaseModel):
    id: Optional[UUID] = None
    title: str
    ingredients: List[str]
    instructions: str
    tags: Optional[List[str]] = None
    image_url: Optional[str] = None 