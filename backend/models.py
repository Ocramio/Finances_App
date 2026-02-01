from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "finances_app_users"

    user_id = Column(Integer, primary_key=True)
    user_email = Column(Text, nullable=False, unique=True)
    user_first_name = Column(Text, nullable=False)
    user_last_name = Column(Text, nullable=False)
    user_hashed_password = Column(Text, nullable=False)
    user_role = Column(Text, nullable=False)
