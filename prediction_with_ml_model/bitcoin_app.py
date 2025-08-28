from fastapi import FastAPI 
from pydantic import BaseModel
# from prediction_with_ml_model.bitcoin import predict_future_close
from .bitcoin import predict_future_close



app =FastAPI() 

class DateInput(BaseModel):
    date : str #eg, 026-01-05


@app.get("/")
def home():
    return {"message" : "welcome to the bitcoin prediction" }

@app.post("/predict")
def predict(input:DateInput):
    predicted_close= predict_future_close(input.date)
    return {"date": input.date , "prediction_close" : predicted_close}
