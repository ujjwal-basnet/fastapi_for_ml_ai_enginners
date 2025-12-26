I plan to add a complete fastapi guide on fastapi of AI / ml enginners 

completed till now : 
   
- [basic](basic)  contains curd delete stuff 

- [ml_prediction](prediction_with_ml_model) contains **bitcoin** price prediction machine leanring model 
    - also contians notebook for ml models under notebook section

- [genai](genai) 
-  contains genai stuff
notebook for model serving 
    -[serve-language-model(basic)](genai/serving_language_model.ipynb)

    - models (real code on how to recive prompt and llm response)
       [model](genai/models.py)
    - controller 
        fastapi code controll flow[controller](genai/main.py)
    
    - ui (streamlit)
        use streamlit for ui 
        [ui](genai/client.py)
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
while the model is loading, the server worker is blocked and cannot process other requests.

    
   
