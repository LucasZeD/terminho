from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class GameHistory(Base):
    __tablename__ = "game_histories"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), nullable=False)
    secret_word = Column(String(5), nullable=False)
    was_sucessful = Column(Boolean, nullable=False)
    guess_count = Column(Integer, nullable=False)
    guesses_list = Column(Text)
    finished_at = Column(DateTime(timezone=True), server_default=func.now())