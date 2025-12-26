import uvicorn
import uvicorn
from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse
from models import load_text_model, generate_text ## resuse 
app = FastAPI()

@app.get("/", include_in_schema=False)
def docs_redirect_controller():
    return RedirectResponse(url="/docs", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/generate/text")
def serve_language_controller(prompt:str)-> str:
    pipe= load_text_model("cpu") 
    output= generate_text(pipe, prompt= prompt)
    return output

# --- SERVER ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000,
        reload=True
    )


