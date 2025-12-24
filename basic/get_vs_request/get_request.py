from fastapi import FastAPI

app= FastAPI()

@app.get("/item/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}



## @app.get decorator defines endpoint 
## {item_id} parameters
## int : type hint 


## get request 
## used to retrive data 
## path parameter information in url 
# does't change server state 
## example: get https://example.com/?item_id=1