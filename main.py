from pkgutil import extend_path
from turtle import title
from fastapi import Body, FastAPI
from pydantic import BaseModel


app = FastAPI()

class Post(BaseModel):
    title: str
    content: str


@app.get("/")
def root():
    return {"message": "Main page test"}

@app.get("/posts")
def get_posts():
    return {"message": "posts page test"}

@app.post("/createpost")
def create_post(Post: Post):
    print(Post)
    return {"new post": "new post created"}
