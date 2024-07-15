from sqlalchemy.orm import Session
from ..import models
from fastapi import HTTPException, status



def create(blog ,db: Session):
    new_blog = models.Blog(title=blog.title, body=blog.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {"message": new_blog}

def delete(id, db:Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return {"message": "Blog deleted"}


def updated(id, blog, db: Session):
    blog_to_update = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    
    blog_to_update.title = blog.title
    blog_to_update.body = blog.body
    db.commit()
    db.refresh(blog_to_update)
    return {"message": blog_to_update}
    

def read_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs

def read_id(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    return blog

    