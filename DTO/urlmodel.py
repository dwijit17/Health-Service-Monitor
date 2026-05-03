from sqlmodel import SQLModel
from pydantic import EmailStr,Field,AnyUrl
class Url_DTO(SQLModel):
    url_link : AnyUrl
    url_name : str = Field(max_length=30)
    user_id : int 