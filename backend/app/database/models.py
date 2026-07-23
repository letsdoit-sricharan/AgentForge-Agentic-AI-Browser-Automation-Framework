from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class DBAgentSession(Base):
    __tablename__ = "agent_sessions"

    session_id = Column(String, primary_key=True)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    goal = Column(JSON, nullable=True) # Serialized Goal
    history = Column(JSON, nullable=True) # Serialized ObservationHistory
    error_message = Column(String, nullable=True)
