from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker

load_dotenv()
database = os.getenv("PostgreeDatabase")
user = os.getenv("PostgreeUser")
password = os.getenv("PostgreePassword")
port = os.getenv("PostgreePort")
engine = create_engine(
    f"postgresql+psycopg2://{user}:{password}@localhost:{port}/{database}"
)

SessionLocal = sessionmaker(bind=engine, autoflush=False,
autocommit=False)

def get_session():
    local_session = SessionLocal()
    try:
        yield local_session
    finally:
        local_session.close()
