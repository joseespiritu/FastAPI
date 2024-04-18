from fastapi import status, HTTPException, APIRouter, Depends
from api.database.db import database, Article
from api.schema.schema import ArticleSchemaIn, ArticleSchemaOut, UserSchemaOut
from typing import List
from auths import get_current_user

router = APIRouter(
    tags=["Articles"]
)

@router.post('/articles/',status_code=status.HTTP_201_CREATED)
async def insert_data(article: ArticleSchemaIn, current_user:UserSchemaOut = Depends(get_current_user)):
    query = Article.insert().values(title=article.title, description=article.description)
    last_record_id = await database.execute(query)
    return {
        **article.dict(),
        "id": last_record_id
    }

@router.get('/articles/', response_model=List[ArticleSchemaOut])
async def get_article(current_user:UserSchemaOut = Depends(get_current_user)):
    query = Article.select()
    return await database.fetch_all(query=query)

@router.get('/articles/{id}', response_model=ArticleSchemaOut)
async def get_article(id:int, current_user:UserSchemaOut = Depends(get_current_user)):
    query = Article.select().where(id==Article.c.id)
    my_article = await database.fetch_one(query=query)
    if not my_article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article does not exist")
    return {**my_article}

@router.put('/articles/{id}')
async def update_data(id:int, article:ArticleSchemaIn, current_user:UserSchemaOut = Depends(get_current_user)):
    query = Article.update().where(Article.c.id == id).values(title=article.title,description=article.description)
    await database.execute(query)
    return {**article.dict(), "id": id}

@router.delete('/articles/{id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_data(id:int, current_user:UserSchemaOut = Depends(get_current_user)):
    query = Article.delete().where(Article.c.id == id)
    await database.execute(query=query)
    return {
        "message": "Data is deleted"
    }