
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class Item(BaseModel):
    name: str


@app.get("/")
def home_page():
    return {"message": "Hellow this is home page"}


@app.post("/")
def root(item: Item):
    name = item.name
    return {"message": f"we have {name}"}
