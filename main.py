from pkgutil import extend_path
from turtle import title
from fastapi import Body, FastAPI, Response,status,HTTPException
from pydantic import BaseModel
from random import randrange


app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: int = None

my_posts = [{"title" : "title of p1", "content" : "example", "id" : 1},{"title" : "title of p2", "content" : "example 2", "id" : 2}]

def find_post(id):
    for i in my_posts:
        if i["id"] == id:
            return i

def delete_post(id):
    for i in range(0,len(my_posts)-1):
        if my_posts[i]['id'] == id:
            return i

@app.get("/")
def root():
    return {"message": "Main page test"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0,100000000)
    my_posts.append(post_dict)
    return {"data" : post_dict}

@app.get("/posts/latest")
def get_lastpost():
    post = my_posts[-1]
    return {"the latest post" : post}

@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={'message' : f"post with {id} does not exist in the current context"})
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message' : f"post with {id} does not exist in the current context"}
    return {"post_detail" : post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def deletePost(id: int):
    index = delete_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={'message' : f"post with {id} does not exist in the current context"})
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int,post: Post):
    index = delete_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={'message' : f"post with {id} does not exist in the current context"})
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"message": post_dict}
