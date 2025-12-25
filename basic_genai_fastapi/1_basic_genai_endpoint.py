from pydantic_ai import Agent
from fastapi import FastAPI 



app = FastAPI()
agent = Agent('google-gla:Gemini 2.5 Flash-Lite')

@app.get('/')
def root_controller():
    return {"status": "healthy"}

