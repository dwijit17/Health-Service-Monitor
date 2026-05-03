from sqlmodel import SQLModel
from pydantic import EmailStr,Field
class User_DTO(SQLModel):
    email : EmailStr
    password : str = Field(min_length=8)

