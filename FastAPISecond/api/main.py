import uvicorn
from fastapi import FastAPI, status, HTTPException
from database.db import metadata, database, engine, Article
from schema.schema import ArticleSchemaIn, ArticleSchemaOut
from typing import List

metadata.create_all(engine)

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post('/articles/',status_code=status.HTTP_201_CREATED)
async def insert_data(article: ArticleSchemaIn):
    query = Article.insert().values(title=article.title, description=article.description)
    last_record_id = await database.execute(query)
    return {
        **article.dict(),
        "id": last_record_id
    }

@app.get('/articles/', response_model=List[ArticleSchemaOut])
async def get_article():
    query = Article.select()
    return await database.fetch_all(query=query)

@app.get('/articles/{id}', response_model=ArticleSchemaOut)
async def get_article(id:int):
    query = Article.select().where(id==Article.c.id)
    my_article = await database.fetch_one(query=query)
    if not my_article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article does not exist")
    return {**my_article}

@app.put('/articles/{id}')
async def update_data(id:int, article:ArticleSchemaIn):
    query = Article.update().where(Article.c.id == id).values(title=article.title,description=article.description)
    await database.execute(query)
    return {**article.dict(), "id": id}

@app.delete('/articles/{id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_data(id:int):
    query = Article.delete().where(Article.c.id == id)
    await database.execute(query=query)
    return {
        "message": "Data is deleted"
    }


if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, log_level="info", reload=True)