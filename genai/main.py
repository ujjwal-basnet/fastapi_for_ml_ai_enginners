import uvicorn
import uvicorn
from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse
from models import load_text_model, generate_text  , load_audio_model , generate_audio ## resuse 
from schemas import VoicePresets
from utils import audio_array_to_buffer
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.get("/", include_in_schema=False)
def docs_redirect_controller():
    return RedirectResponse(url="/docs", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/generate/text")
def serve_language_controller(prompt:str)-> str:
    pipe= load_text_model("cpu") 
    output= generate_text(pipe, prompt= prompt)
    return output


@app.get(
    "/generate/audio",
    responses=  {status.HTTP_200_OK: {'content' : {'audio/wav': {}}}},
    response_class = StreamingResponse,
)
def serve_text_to_audio_model_controller(
    prompt: str,
    preset: VoicePresets = "v2/en_speaker_1"):

    process , model= load_audio_model()
    output, sample_rate= generate_audio(process, model , prompt , preset)
    return StreamingResponse(
        audio_array_to_buffer(output, sample_rate) , media_type="audio/wav"
    )



# --- SERVER ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000,
        reload=True
    )


