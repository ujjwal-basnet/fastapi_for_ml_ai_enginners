from fastapi import FastAPI 


app = FastAPI() 
@app.get("/public-search/")
async def public_search(query: str, category: str = "all"):
    return {"results": f"Showing {category} results for '{query}'"}