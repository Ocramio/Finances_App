from sqlalchemy import Column, Integer, Text, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "finances_app_users"

    user_id = Column(Integer, primary_key=True)
    user_email = Column(Text, nullable=False, unique=True)
    user_first_name = Column(Text, nullable=False)
    user_last_name = Column(Text, nullable=False)
    user_hashed_password = Column(Text, nullable=False)
    user_role = Column(Text, nullable=False)

    expenses = relationship("Expense", back_populates="user")

class Expense(Base):
    __tablename__ = "finances_app_expenses"

    expense_id = Column(Integer, primary_key=True, index=True)
    expense_type = Column(Text, nullable=False)
    expense_value = Column(Float, nullable=False)
    expense_description = Column(Text)
    user_id = Column(
        Integer,
        ForeignKey("finances_app_users.user_id"),
        nullable=False
    )

    user = relationship("User", back_populates="expenses")

