from fastapi import FastAPI, Depends, HTTPException, status
from typing import Optional
from . import schemas
from .import models, schemas
from .database import engine ,SessionLocal, get_db
from sqlalchemy.orm import Session
app = FastAPI()


models.Base.metadata.create_all(engine)


@app.post('/blog', status_code= status.HTTP_201_CREATED)
def create_blog(blog: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog.title, body=blog.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {"message": new_blog}


# @app.delete("/blog/{id}",status_code= status.HTTP_204_NO_CONTENT)
# def delete_blog(id , db: Session = Depends(get_db)):
#     db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session= False)
#     db.commit()
#     return {"Blog" : "Deleted"}


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return 'done'


@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED)
def update_blog(id : int ,blog :schemas.Blog,db: Session = Depends(get_db)):
    blog_to_update = db.query(models.Blog).filter(models.Blog.id == id).first().update({"title" : "updated"})
    if blog_to_update:
        blog_to_update.title = blog.title
        blog_to_update.body = blog.body
        db.commit()
        db.refresh(blog_to_update)
        return {"message": blog_to_update}
    return {"message": f"Blog with id {id} not found"} # bulk poeration thats why doing it this way 



@app.get("/blog")
def reading_blog(db : Session = Depends(get_db)):
    blogs=db.query(models.Blog).all()
    return blogs


@app.get('/blog/{id}')
def reading_id(id , db :Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id ==id ).first()
    if not blog :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the id with {id} is not found")
    #    return {"details of error" : f" the  id with {id} is not available"}
        
    return  blog
    
    