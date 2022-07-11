from click import get_current_context
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from fastapi import Body, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from typing import List, Optional
from sqlalchemy import func


# ********************************
# These were only necessary when we had our posts in a list/memory.
# They are no longer necessary
# def find_post(id):
#     # This worked if we had a list in memory, but won't really work for a database
#     # for post in my_posts:
#     #     if post['id'] == id:
#     #         return post
#     cursor.execute("""SELECT * FROM posts WHERE id=%s""", (id))
#     fetched_post = cursor.fetchone()
#     return fetched_post


# def find_index_of_post(id):
#     for index, post in enumerate(my_posts):
#         if post['id'] == id:
#             return index
# ********************************

# -------- Home Page ---------

router = APIRouter(prefix="/posts", tags=['Posts'])


# ------- Get All Posts -------

# , response_model=List[schemas.PostOut]
@ router.get("/", response_model=List[schemas.PostOut])
# This is the function definition if using Raw SQL
# def get_posts():
#
# This is the function definition if using ORM
def get_posts(db: Session = Depends(get_db),
              current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # ******* Using Raw SQL ***********
    # cursor.execute("""SELECT * FROM posts;""")
    # posts = cursor.fetchall()

    # ******* Using ORM **************

    print(limit)
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip)

    print(posts)

    return posts.all()

# --------- Get Individual Post --------
# the id here is called a path parameter


@ router.get("/{id}", response_model=schemas.PostOut)
# This is the function definition if using Raw SQL
# def get_individual_post(id: int, response: Response):
#
# This is the function definition if using ORM
def get_individual_post(id: int, db: Session = Depends(get_db),
                        current_user: int = Depends(oauth2.get_current_user)):
    # ******* Using Raw SQL ***********
    # cursor.execute("""SELECT * FROM posts WHERE id=%s""", (str(id)))
    # post = cursor.fetchone()
    #
    # ******* Using ORM **************

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id,
        isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return post

# ------- Create New Post --------

# !! If we want to have a schema for a respone, but it in the decorator!


@ router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
# This is the function definition if using Raw SQL
# def create_posts(post: Post):
#
# This is the function definition if using ORM
def create_posts(post: schemas.Post, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    # ******* Using Raw SQL ***********
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *;""",
    #              (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    # ******* Using ORM **************
    # !! This method below works just fine, but if there are many columns it is
    # !! Inefficient. A better method is to unpack the dictionary, commented below.

    new_post = models.Post(
        title=post.title, content=post.content, published=post.published, owner_id=current_user.id)
    # !!!!!  Better method:
    # new_post = models.Post(**post.dict()) # This will unpack the dictionary created
    # With an ORM, still have to commit
    db.add(new_post)
    db.commit()
    # db.refresh effectively works as RETURNING
    db.refresh(new_post)
    return new_post


# --------- Delete Individual Post -------


@ router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
# This is the function definition if using Raw SQL
# def delete_post(id: int):
# def get_individual_post(id: int, response: Response):
#
# This is the function definition if using ORM
def delete_post(id: int, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # ******* Using Raw SQL ***********
    # cursor.execute(
    #   """DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # del_post = cursor.fetchone()
    #
    # ******* Using ORM **************
    del_post_query = db.query(models.Post).filter(models.Post.id == id)
    del_post = del_post_query.first()
    if del_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    # conn.commit() # for Raw SQL
    if del_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action.")
    del_post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# ----------- Update Individual Post ---------


@ router.put("/{id}", response_model=schemas.PostResponse)
# This is the function definition if using Raw SQL
# def update_individual_post(id: int, post: Post):
#
# This is the function definition if using ORM
def update_individual_post(id: int, post: schemas.Post, db: Session = Depends(get_db),
                           current_user: int = Depends(oauth2.get_current_user)):
    # ******* Using Raw SQL ***********
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s
    # WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    #
    # ******* Using ORM **************
    updated_post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = updated_post_query.first()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action.")
    # conn.commit() # for Raw SQL
    updated_post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return updated_post_query.first()
