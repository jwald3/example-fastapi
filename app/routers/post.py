from sqlalchemy import func
from app import oauth2
from .. import models, schemas, oauth2
from fastapi import Depends, Response, status, HTTPException, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session
from ..database import get_db


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
            limit: int = 10, skip: int = 0, search: Optional[str] = ""): 
    
    # to only return posts of current user
    # posts = db.query(models.Post).filter(models.Post.user_id == current_user.id).all()
    
    # to return all posts regardless of user id
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True
        ).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return results



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):

    new_post = models.Post(user_id=current_user.id, **post.dict()) # unpacks all properties from post object

    db.add(new_post)        # stage to db
    db.commit()             # commit changes
    db.refresh(new_post)    # repopulates "new_post" with post data
 
    return new_post



@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int,  db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True
        ).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"post with the id {id} was not found")

    return post



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,                                                # ID of post to delete
                db: Session = Depends(get_db),                          # open session of db
                current_user: int = Depends(oauth2.get_current_user)    # find current active user 
                ):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    # catch non-existing post error
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,              
                            detail=f"post with the id: {id} does not exist.")   

    # catch user attempting to delete other users' posts
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action"
        )

    # delete post if it exists and belongs to current user
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)   



@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int,                                                # ID of post
                updated_post: schemas.PostCreate,                       # parse request as a post schema
                db: Session = Depends(get_db),                          # make connection to db
                current_user: int = Depends(oauth2.get_current_user)    # find current active user
            ):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    # catch non-existing post error
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with the id: {id} does not exist.")

    # catch user attempting to update other users' posts
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action"
        )

    # update post if it exists and belongs to current user
    post_query.update(updated_post.dict(), synchronize_session=False)
    
    db.commit()

    return post_query.first()