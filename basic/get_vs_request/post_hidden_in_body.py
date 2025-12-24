from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class QueryInput(BaseModel):
    query:str

@app.post("/private-search/")
async def private_search(data: QueryInput):
    return {"result": f"confidential result for '{data.query}' "}
