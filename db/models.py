from sqlmodel import SQLModel,Field
from datetime import datetime,timezone
from sqlalchemy import UniqueConstraint
from enum import Enum

class Status(str , Enum):
    up = "up"
    down = "down"

class User(SQLModel,table=True):
    id : int | None = Field(default=None,primary_key=True)
    email : str = Field(unique=True,nullable=False)
    password_hash : str

class Url(SQLModel,table=True):
    id : int | None = Field(default=None,primary_key=True)
    url_link : str = Field(unique=True,nullable=False)
    url_name : str = Field(max_length=255)
    created_at : datetime = Field(default_factory=lambda : datetime.now(timezone.utc))

class UserUrl(SQLModel,table=True):
    __table_args__ = (UniqueConstraint("user_id", "url_id"),)
    id : int | None = Field(default=None,primary_key=True)
    user_id : int = Field(foreign_key="user.id")
    url_id : int = Field(foreign_key="url.id")
    added_at : datetime =  Field(default_factory=lambda :  datetime.now(timezone.utc))

class HealthLog(SQLModel,table=True):
    id : int | None = Field(default=None,primary_key=True)
    url_id : int = Field(foreign_key="url.id")
    status : Status = Field(nullable=False)
    response_time_ms: int | None = None
    checked_at : datetime = Field(default_factory=lambda :  datetime.now(timezone.utc))
