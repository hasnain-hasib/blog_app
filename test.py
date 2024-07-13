from fastapi import FastAPI, Query
from typing import Optional
from pydantic import BaseModel



app= FastAPI()

class Data(BaseModel):
    id : int
    name: str
    age : Optional[int]= None


@app.post('/test', response_model=Data)
def posting(request_body = Data, name = Data, age = Data):
    return {"The request body should look like this " : request_body}
