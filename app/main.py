from fastapi import FastAPI, HTTPException, status
from fastapi.params import Body
from random import randrange
from .models import Post, curs, conn
from .script import my_posts, find_post, find_index_post

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    curs.execute("""SELECT * FROM posts """)
    posts = curs.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    curs.execute(
        """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    conn.commit()
    return {"data": "created post"}


@app.get("/posts/{id}")
def get_post(id: int):
    curs.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    post = curs.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    return {"post details": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    curs.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    deleted_post = curs.fetchone()
    conn.commit()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")
    return {"messages": "Post successfully deleted"}


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    curs.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
                 (post.title, post.content, post.published, (str(id))))
    updated_post = curs.fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")

    return {"message": "Updated Successfully"}
