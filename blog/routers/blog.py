from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, models
from ..database import get_db
from ..repository import blog

router = APIRouter(
    tags=['Blog Module']
)


@router.post('/blog', status_code=status.HTTP_201_CREATED)
def create_blog(blogs: schemas.Blog, db: Session = Depends(get_db)):
    return blog.create(blogs, db)

@router.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    return blog.delete(id, db)

@router.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, blog: schemas.Blog, db: Session = Depends(get_db)):
    return blog.updated(id, blog, db) 
    
@router.get("/blog", response_model=List[schemas.ShowBlog])
def all_blogs(db: Session = Depends(get_db)):

    return blog.read_all(db)

@router.get("/blog/{id}", response_model=schemas.ShowBlog)
def blog_id(id: int, db: Session = Depends(get_db)):

    return blog.read_id(id,db)
