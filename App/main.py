# sqlalchey and fastapi
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from .models import Base, User, Study_Session, Session_notes
from datetime import datetime
# from flask_cors import CORS
from fastapi.middleware.cors import CORSMiddleware

# Database setup
MYDatabase = "sqlite:///./sessionManager.sqlite"  
engine = create_engine(MYDatabase, connect_args={"check_same_thread": False})
myLocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialize FastAPI app
apk = FastAPI()

origins = [
    "http://localhost:5173"
]
apk.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  
)
# Dependency to get the database session
def get_db():
    db = myLocalSession()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)

# Pydantic models for validating the user input
class UserCreate(BaseModel):
    name: str
    email: str
    password: str

    class Config:
        orm_mode = True

class StudySessionCreate(BaseModel):
    title: str
    date: datetime
    duration: int
    user_id: int

    class Config:
        orm_mode = True

class SessionNoteCreate(BaseModel):
    note_context: str
    session_id: int

    class Config:
        orm_mode = True


# Routes for User
@apk.post("/users/")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if the email already exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(name=user.name, email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@apk.get("/users/{user_id}")
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@apk.get("/users/")
async def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@apk.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Delete all associated study sessions and session notes
    db_sessions = db.query(Study_Session).filter(Study_Session.user_id == user_id).all()
    for session in db_sessions:
        db_notes = db.query(Session_notes).filter(Session_notes.session_id == session.id).all()
        for note in db_notes:
            db.delete(note)  # delate associated notes
        db.delete(session)  # delete associated study session

    db.delete(db_user)  # delete the user
    db.commit()
    return {"message": "User and associated data deleted successfully"}

@apk.patch("/users/{user_id}")
async def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_user.name = user.name
    db_user.email = user.email
    db_user.password = user.password
    db.commit()
    db.refresh(db_user)
    return db_user

# Routes for Study Session
@apk.post("/study_sessions/")
async def create_study_session(session: StudySessionCreate, db: Session = Depends(get_db)):
    new_session = Study_Session(title=session.title, date=session.date, duration=session.duration, user_id=session.user_id)
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session

@apk.get("/study_sessions/{session_id}")
async def read_study_session(session_id: int, db: Session = Depends(get_db)):
    db_session = db.query(Study_Session).filter(Study_Session.id == session_id).first()
    if db_session is None:
        raise HTTPException(status_code=404, detail="Study session not found")
    return db_session

@apk.get("/study_sessions/")
async def get_study_sessions(db: Session = Depends(get_db)):
    sessions = db.query(Study_Session).all()
    return sessions

@apk.delete("/study_sessions/{session_id}")
async def delete_study_session(session_id: int, db: Session = Depends(get_db)):
    db_session = db.query(Study_Session).filter(Study_Session.id == session_id).first()
    if db_session is None:
        raise HTTPException(status_code=404, detail="Study session not found")
    
    # Delete all associated session notes
    db_notes = db.query(Session_notes).filter(Session_notes.session_id == session_id).all()
    for note in db_notes:
        db.delete(note)

    db.delete(db_session)  # delete a study session
    db.commit()
    return {"message": "Study session and associated notes deleted successfully"}

@apk.patch("/study_sessions/{session_id}")
async def update_study_session(session_id: int, session: StudySessionCreate, db: Session = Depends(get_db)):
    db_session = db.query(Study_Session).filter(Study_Session.id == session_id).first()
    if db_session is None:
        raise HTTPException(status_code=404, detail="Study session not found")
    
    db_session.title = session.title
    db_session.date = session.date
    db_session.duration = session.duration
    db.commit()
    db.refresh(db_session)
    return db_session


# Routes for Session Notes
@apk.post("/session_notes/")
async def create_session_note(note: SessionNoteCreate, db: Session = Depends(get_db)):
    # check if it exists using the ID ...
    existing_note = db.query(Session_notes).filter(
        Session_notes.note_context == note.note_context,
        Session_notes.session_id == note.session_id
    ).first()

    if existing_note:
        raise HTTPException(status_code=400, detail="Session note already exists.")

    # Create the new note if it doesn't exist
    new_note = Session_notes(note_context=note.note_context, session_id=note.session_id)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note



@apk.get("/session_notes/{note_id}")
async def read_session_note(note_id: int, db: Session = Depends(get_db)):
    db_note = db.query(Session_notes).filter(Session_notes.id == note_id).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Session note not found")
    return db_note

@apk.get("/session_notes/")
async def get_session_notes(db: Session = Depends(get_db)):
    notes = db.query(Session_notes).all()
    return notes

@apk.delete("/session_notes/{note_id}")
async def delete_session_note(note_id: int, db: Session = Depends(get_db)):
    db_note = db.query(Session_notes).filter(Session_notes.id == note_id).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Session note not found")
    
    db.delete(db_note)  # Delete the session note
    db.commit()
    return {"message": "Session note deleted successfully"}

@apk.patch("/session_notes/{note_id}")
async def update_session_note(note_id: int, note: SessionNoteCreate, db: Session = Depends(get_db)):
    db_note = db.query(Session_notes).filter(Session_notes.id == note_id).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Session note not found")
    
    db_note.note_context = note.note_context
    db.commit()
    db.refresh(db_note)
    return db_note
