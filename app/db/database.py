'''
DATABASE FOR HISTORICAL DATA

TABLE: user_stats
usr_id varchar(255) PK # user id
ttl_gms INT # total games played
gms_won INT # total games won
crr_strk INT # current streak
lgst_strk INT # longest streak
~lst_plyd TIMESTAMP~

TABLE: game_histories

TABLE: message_logs
id SERIAl PK
user_id VARCHAR(255)
direction TEXT CHECK (direction IN ('in', 'out'))
message TEXT
timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
'''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()