from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

class Item(BaseModel):
    name: str
    quantity: Optional[int] = 0

app = FastAPI()

items = {"iphone": Item(name="iphone", quantity=100)}

@app.get("/items")
def read(name: str):
    if name not in items:
        raise HTTPException(status_code=400, detail='item not found')
    return items[name]
