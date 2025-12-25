from sql_lite_database import Base
import uvicorn
from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session

# --- 1. CLEANUP PREVIOUS RUNS ---
if 'server' in globals():
    server.should_exit = True
    # Give it a moment to release the port
    await asyncio.sleep(1) 


# --- DATABASE SETUP ---
DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- MODELS ---
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)

    messages = relationship("Message", back_populates="user")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="messages")


Base.metadata.create_all(bind=engine)

# --- APP ---
app = FastAPI()


@app.get("/", include_in_schema=False)
def docs_redirect_controller():
    return RedirectResponse(url="/docs", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/users")
def create_user(email: str, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="User already exists")

    user = User(email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.post("/users/{email}/messages")
def create_message(email: str, content: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    msg = Message(content=content, user_id=user.id)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg


@app.get("/users/{email}/messages")
def get_messages(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user.messages


# --- SERVER ---
config = uvicorn.Config(app, host="127.0.0.1", port=8000)
server = uvicorn.Server(config)

loop = asyncio.get_event_loop()
loop.create_task(server.serve())

print("Server running on http://127.0.0.1:8000")
