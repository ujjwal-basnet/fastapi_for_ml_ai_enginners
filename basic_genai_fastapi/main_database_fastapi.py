import uvicorn
from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

import models_sqlite as models
from database_sqlite import engine, get_db

# Sync the database schema (create tables)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/", include_in_schema=False)
def docs_redirect():
    return RedirectResponse(url="/docs", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/users")
def create_user(email: str, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = models.User(email=email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/users/{email}/messages")
def create_message(email: str, content: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_msg = models.Message(content=content, user_id=user.id)
    db.add(new_msg)
    db.commit()
    db.refresh(new_msg)
    return new_msg

@app.get("/users/{email}/messages")
def get_messages(email: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # SQLAlchemy objects can be returned directly by FastAPI
    return user.messages

if __name__ == "__main__":
    uvicorn.run("main_database_fastapi:app", host="127.0.0.1", port=8002, reload=True)