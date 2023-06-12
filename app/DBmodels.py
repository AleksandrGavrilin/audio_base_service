from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
import os

database = os.getenv('DB_URI', "postgresql://audio_user:cfytr666131@postgres_container/audiodb")


# Создание базы данных:
Base = declarative_base()
engine = create_engine(database)
Session = sessionmaker(autoflush=False, bind=engine)


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    UUID = Column(String, nullable=False, default="")
    name = Column(String, nullable=False, default="")


class Audio(Base):
    __tablename__ = "audio"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    UUID = Column(String, nullable=False, default="")
    user_id = Column(Integer, ForeignKey('users.id'))
    data = Column(LargeBinary)


Base.metadata.create_all(bind=engine)
