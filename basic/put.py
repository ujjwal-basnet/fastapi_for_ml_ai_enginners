

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

reviews_table = {
    1: {"_id": 1, "movie": "Inception", "num_stars": 5, "text": "Great!"},
    2: {"_id": 2, "movie": "Matrix", "num_stars": 4, "text": "Awesome!"}
}

class Dbreview(BaseModel):
    movie: str
    num_stars: int
    text: str
    review_id: int

@app.get("/")
def home_page():
    return "Welcome to the home page"


@app.put("/reviews/")
def update_review(review: Dbreview):
    reviews_table[review.review_id] = {
        "_id": review.review_id,
        "movie": review.movie,
        "num_stars": review.num_stars,
        "text": review.text
    }
    return {"status": "updated", "review": reviews_table[review.review_id]}

@app.get("/reviews")
def get_all_reviews():
    return reviews_table
