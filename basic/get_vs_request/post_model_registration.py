from fastapi import FastAPI 
from pydantic import BaseModel 

class ModelInfo(BaseModel):
    model_id: int 
    model_name: str
    description: str 
app = FastAPI()

#model database 
model_db= {} 

# specify the status code for sucessfull post request 
@app.post("/register-model", status_code= 201)
def register_model(model_info: ModelInfo):
    model_db[model_info.model_id]= model_info.dict()
    return {"message": "model registered sucessfully", "model": model_info.dict()} , 201
