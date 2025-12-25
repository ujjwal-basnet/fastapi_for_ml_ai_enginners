from fastapi.responses import RedirectResponse
from pydantic import BaseModel, validator
from fastapi import FastAPI, status

class UserCreate(BaseModel):
    username: str
    password: str

    @validator('password') 
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(char.isdigit() for char in value):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isupper() for char in value):
            raise ValueError('Password must contain at least one uppercase letter')
        return value 

app = FastAPI()

@app.post("/users")
async def create_user_controller(user: UserCreate):
    return {"username": user.username, "message": "Account successfully created"}

@app.get("/" , include_in_schema=False)
def dos_redirect_controller():
    return RedirectResponse(url="/docs", status_code=status.HTTP_303_SEE_OTHER)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "data_validation:app",  # Ensure this path matches your directory structure
        host="127.0.0.1",
        port=8000,
        reload=True
    )
