from fastapi import FastAPI, HTTPException, status
from tortoise.contrib.fastapi import register_tortoise, HTTPNotFoundError
import uvicorn
from api.models import ArticleIn_Pydantic, Article, Article_Pydantic
from pydantic import BaseModel

app = FastAPI()

class Status(BaseModel):
    message: str

@app.get('/api/articles/')
async def get_articles():
    return await Article_Pydantic.from_queryset(Article.all())

@app.post('/api/articles/')
async def insert_data(article:ArticleIn_Pydantic):
    article_obj = await Article.create(**article.dict(exclude_unset=True))
    return await Article_Pydantic.from_tortoise_orm(article_obj)

@app.get('/api/articles/{id}', responses={404, {"model":HTTPNotFoundError}})
async def get_details(id:int):
    return await Article_Pydantic.from_queryset_single(Article.get(id=id))

@app.put('/api/articles/{id}', responses={404:{"model":HTTPNotFoundError}})
async def update_data(id:int, article:ArticleIn_Pydantic):
    await Article.filter(id=id).update(**article.dict(exclude_unset=True))
    return await Article_Pydantic.from_queryset_single(Article.get(id=id))

@app.delete('/api/articles/{id}', response_model=Status, responses={404:{"model":HTTPNotFoundError}})
async def delete_data(id:int):
    deleted_data = await Article.filter(id=id).delete()
    if not deleted_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Article {id} not found")

    return Status(message=f"Article {id} deleted")


register_tortoise(
    app,
    db_url="mysql://root:@localhost:3306/fastapi",
    modules={"models":["api.models"]},
    generate_schemas=True,
    add_exception_handlers=True
)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, log_level="info", reload=True)