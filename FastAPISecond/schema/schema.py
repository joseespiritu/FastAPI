from pydantic import BaseModel

class ArticleSchemaIn(BaseModel):
    title: str
    description: str

class ArticleSchemaOut(ArticleSchemaIn):
    title: str
    description: str