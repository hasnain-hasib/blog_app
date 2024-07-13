from fastapi import FastAPI
from typing import Optional
from . import schemas
from .import models, schemas
from .database import engine
app = FastAPI()


models.Base.metadata.create_all(engine)


@app.post('/blog')
def create( bloggingg: schemas.Blog):
    return {"here are some info about the blog " :bloggingg}


