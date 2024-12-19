# models.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    email = Column(Text, nullable=False, unique=True)
    password = Column(String, nullable=False, unique=True)

    # Relationship with Study_Session
    studySessions = relationship('Study_Session', back_populates='user')


class Study_Session(Base):
    __tablename__ = 'study_session'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    duration = Column(Integer, nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'))

    # Relationships
    user = relationship('User', back_populates='studySessions')
    sessionNotes = relationship('Session_notes', back_populates='studySession')


class Session_notes(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True, index=True)
    note_context = Column(Text, nullable=False)
    session_id = Column(Integer, ForeignKey('study_session.id'))

    # Relationship with Study_Session
    studySession = relationship('Study_Session', back_populates='sessionNotes')
