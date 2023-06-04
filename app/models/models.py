from datetime import datetime
from sqlalchemy import String, Integer, TIMESTAMP, Column
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Question(Base):
    __tablename__ = "questions"

    id = Column("id", Integer, primary_key=True, index=True)
    text = Column("text", String)
    answer = Column("answer", String)
    created_at = Column("created_at", TIMESTAMP, default=datetime.utcnow)

