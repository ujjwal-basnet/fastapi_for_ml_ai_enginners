
""" 
example of get request :  https://www.google.com:80/search?q=fastapi 
host : www.google.com 
port : 80 
path , /search 
query string : ?q=fastapi 

"""


""" building first get endpoint to acess the input 

which takes input as name and return dict"""

from fastapi import FastAPI 

app = FastAPI() 

@app.get("/") 
def root(name:str = "ujjwal"): 
    return {"message": "Hellow {ujjwal}"}


""" 
now to change the name , 

    curl \
    -H 'Content-Type: application/json' \
    http://localhost:8000?name=ram


""" 
