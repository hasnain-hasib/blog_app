from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext

from .. import schemas, models

from ..database import get_db
from ..hashing import Hash

router = APIRouter(
    prefix="/user",
    tags=['User Module']
)


@router.post("/", response_model=schemas.ShowUser)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    
    new_user = models.User(name=user.name, email=user.email, password=Hash.bcrypt(user.password))
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/", response_model=List[schemas.ShowUser])
def read_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.get("/{id}", response_model=schemas.ShowUser)
def read_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return user   

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    user_to_delete = db.query(models.User).filter(models.User.id == id).first()
    if not user_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    
    db.delete(user_to_delete)
    db.commit()
    return {"message": "User deleted successfully"}
