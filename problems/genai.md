## problem in genai 
    ``` 
    @app.get("/generate/text")
    def serve_language_controller(prompt: str) -> str:
        pipe = load_text_model("cpu")
        output = generate_text(pipe, prompt=prompt)
        return output
    ``` 

    
here everytime streamlit sends aa request to fastapi 
  - fastapi recives ``/generate/text``
  - ``load_text_model()`` is called 
  - Hugging Face pipeline:

        -downloads (if not cached)
        -loads ~1.1B parameters from disk
        -deserializes weights
        -allocates CPU/GPU memory

that means evertime we send request -> it load models everytime... 

loading and unloading a large LLM per request is slow, memory-heavy, and I/O-blocking.
while the model is loading, the server worker is blocked and cannot process other requests