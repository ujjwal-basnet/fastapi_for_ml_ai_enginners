from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel 
from transformers import pipeline, AutoTokenizer,  AutoModelForSequenceClassification
from contextlib import asynccontextmanager 
import numpy as np 
import torch 
import logging 

#configute logging 
logging.basicConfig(
    level= logging.INFO
    )
logger = logging.getLogger(__name__)


#define lifespan manager 
@asynccontextmanager
async def lifespan(app:FastAPI):
    logger.info("loading ml models")
    app.state.qa_model= pipeline(
        task="question-answering",
        model="distilbert/distilbert-base-uncased-distilled-squad")
    
    app.state.sentiment_model= pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english"  )
    


    #Load tokenizer separatly for advance use 
    app.state.tokenizer= AutoTokenizer.from_pretrained("distilbert-base-uncased")
    
    logger.info(
        msg="Model loaded Sucessfully")
    
    yield 
    logger.info("cleaning up resources")
    del app.state.qa_model 
    del app.sentiment_model
    del app.text_generator 
    torch.cuda.empty_cache() if torch.cuda.is_available() else None 


#initilized FastAPI with lifespan 
app= FastAPI(
    title= "Advance Ml API",
    description="API demonstrating GET/POst with Hugging Face Transformers",
    version="1.0.0",
    lifespan=lifespan 
)


class SentimentResponse(BaseModel):
    text: str 
    label: str 
    confidence: float 
    entropy: float 


@app.get(path="/sentiment/", response_model=SentimentResponse)
async def analyze_sentiment(text: str= Query(... ,
                     min_length= 5, 
                     max_length=500,
                     example="I love you"),
                     
                     detailed : bool= Query(False, description="Return entropy metric")):
    
    """ Get Endpoints for text Sentiment Analysis"""
    try: 
        result= app.state.sentiment_model(text)[0]
        entropy= -np.log(result['score']) if detailed else None 

        return {
            "text": text ,
            "label": result['label'],
            "confidence": result["score"],
            "entropy": entropy

        }
    
    except Exception as e : 
        logger.error(f"Sentiment analysis failed: {str(e)}")
        raise HTTPException(500, "Analysis failed")
    

    ### get endpoints for  question anaswering 

@app.get(path= "/qa/")
async def question_answering( context: str = Query(..., min_length=20,  example="Fast APi is a modern web framework for Building API for python"),
    questions: str= Query(..., example="what is FastApi")):

    ####### get endpoints question answering ######### 
    try: 
        result= app.state.qa_model(question= questions, context= context)

        #calcualte the answer coverage 
        coverage= (result['end'] - result['start']/len(context))

        return {
            "question": questions ,
            "answer": result['answer'],
            "confidience": result['score'],
            "start_index": result['start'],
            "end_index":result['end'],
            "coverage": coverage
        }
    
    except Exception as e:
        logger.error(f"QA failed {str(e)}")
        raise HTTPException(500, "question answering failed")
    





    
