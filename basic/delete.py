
from pydantic import BaseModel 
from fastapi import FastAPI 

app= FastAPI()

reviews_table = {
    1: {"_id": 1, "movie": "Inception", "num_stars": 5, "text": "Great!"},
    2: {"_id": 2, "movie": "Matrix", "num_stars": 4, "text": "Awesome!"}}

class ReviewDelete(BaseModel):
    review_id: int 

@app.get("/")
def home_page():
    return "Greeting this is the demonstration of the delete "


@app.delete("/reviews/")
def delete_review(key: ReviewDelete):
    if key.review_id in reviews_table:

        deleted= reviews_table.pop(key.review_id)
        return f" we have sucessfully dedlete \n {deleted} " 

    return {'error': 'review not deleted'}

@app.get("/reviews/")
def show_reviews():
    return reviews_table



