from fastapi import FastAPI
from pydantic import BaseModel

class Blog(BaseModel):
    title : str
    body :str