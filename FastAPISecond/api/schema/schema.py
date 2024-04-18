from pydantic import BaseModel
from typing import Union

class ArticleSchemaIn(BaseModel):
    title: str
    description: str

class ArticleSchemaOut(ArticleSchemaIn):
    title: str
    description: str

class UserSchemaIn(BaseModel):
    username: str
    password: str

class UserSchemaOut(BaseModel):
    id: int
    username: str

class LoginSchema(BaseModel):
    username: str
    password: str


class TokenData(BaseModel):
    username: Union[str, None] = None