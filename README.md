## Links ...
FRONTEND LINK : [https://charlesnjoroge8822.github.io/My-Session.-FRONTEND/](https://github.com/CharlesNJoroge8822/My-Session.-FRONTEND)
SLIDES LINK : https://www.canva.com/design/DAGZTHhjoYs/1ZeHFIB79ejKCP2Z0D_1Vg/edit?utm_content=DAGZTHhjoYs&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton
SREENCAST LINK : https://www.loom.com/share/18cc4569aaa54172a07f1e13448c72f9?sid=51a7a980-2660-44b2-ae6a-e5088c72867a
                : https://www.loom.com/share/63c2f3f96839463185c0ccf8bbc6b6a7?sid=7f6aa0b5-1ecb-4b7e-b15f-ae4ffd8d4a14

Study Session Manager
This project allows users to manage their study sessions, track notes, and update their personal information. It consists of a backend built with FastAPI and a frontend created with React (Vite).

Project Structure
Backend (FastAPI + SQLAlchemy)
Backend URL: http://127.0.0.1:8000
The backend is responsible for managing the users, study sessions, and session notes.
The backend interacts with an SQLite database (sessionManager.sqlite) using SQLAlchemy ORM.
Main Files:
main.py: The FastAPI app that defines all the endpoints and handles CRUD operations for users, study sessions, and session notes.
models.py: Defines the database models (User, Study_Session, Session_notes) using SQLAlchemy.
sqlalchemy.py: Responsible for setting up the database and establishing connections using SQLAlchemy.
Pydantic models: Used for data validation in FastAPI routes (e.g., UserCreate, StudySessionCreate, etc.).
Routes:
User Routes:

POST /users/: Create a new user.
GET /users/{user_id}: Get a user by their ID.
GET /users/: Get all users.
PATCH /users/{user_id}: Update a user's information.
DELETE /users/{user_id}: Delete a user and their associated study sessions and notes.
Study Session Routes:

POST /study_sessions/: Create a new study session.
GET /study_sessions/{session_id}: Get a study session by its ID.
GET /study_sessions/: Get all study sessions.
PATCH /study_sessions/{session_id}: Update a study session.
DELETE /study_sessions/{session_id}: Delete a study session and its associated notes.
Session Notes Routes:

POST /session_notes/: Create a new session note.
GET /session_notes/{note_id}: Get a session note by its ID.
GET /session_notes/: Get all session notes.
PATCH /session_notes/{note_id}: Update a session note.
DELETE /session_notes/{note_id}: Delete a session note.

