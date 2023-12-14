from fastapi import FastAPI, Query
from fastapi.openapi.models import Info, ExternalDocumentation
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
from typing import Optional, List

# Each post might have an id, title, and content
posts_db = [
    {
        "id": 1,
        "title": "First Post",
        "content": "This is the first post."
    }
]

# Each comment might have an id, post_id (to associate it with a post), and content
comments_db = [
    {
        "id": 1,
        "post_id": 1,
        "content": "This is a comment on the first post."
    }
]

# Each like might have an id and post_id (to associate it with a post)
likes_db = [
    {
        "id": 1,
        "post_id": 1
    }
]

class Post(BaseModel):
    id: int
    title: str
    content: str

class Comment(BaseModel):
    id: int
    post_id: int
    content: str

class Like(BaseModel):
    id: int
    post_id: int

app = FastAPI(
    title="BizOpti API",
    description="An API to automate your Business Decisions decisions.",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Pricing",
            "description": "Price ERP implementations automatically.",
        }
    ],
    info=Info(
        title="BizOpti API",
        version="1.0.0",
        description="An API to automate Business decisions.",
        terms_of_service="https://erpGPT-api.onrender.com/terms",
        contact={
            "name": "Matt Majestic",
            "url": "https://www.youtube.com/@majesticcoding",
        },
        license={
            "name": "Apache 2.0",
            "url": "https://www.apache.org/licenses/LICENSE-2.0",
        },
    ),
    external_docs=ExternalDocumentation(
        description="Find more information here",
        url="https://erpGPT-api.onrender.com/docs",
    ),
)

origins = [
    "http://localhost:3000",  # React app
    "https://bizopti.xyz",  # Production site
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def price_erp():
    return {"price": 10}

@app.post("/posts/")
async def create_post(post: Post):
    posts_db.append(post.dict())
    return post

@app.get("/posts/")
async def read_posts():
    return posts_db

@app.put("/posts/{post_id}")
async def update_post(post_id: int, post: Post):
    for index, existing_post in enumerate(posts_db):
        if existing_post['id'] == post_id:
            posts_db[index] = post.dict()
            return post
    return {"error": "Post not found"}

@app.delete("/posts/{post_id}")
async def delete_post(post_id: int):
    for index, existing_post in enumerate(posts_db):
        if existing_post['id'] == post_id:
            posts_db.pop(index)
            return {"message": "Post deleted"}
    return {"error": "Post not found"}

@app.post("/comments/")
async def create_comment(comment: Comment):
    comments_db.append(comment.dict())
    return comment

@app.get("/comments/")
async def read_comments():
    return comments_db

@app.post("/likes/")
async def create_like(like: Like):
    likes_db.append(like.dict())
    return like

@app.get("/likes/")
async def read_likes():
    return likes_db

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
