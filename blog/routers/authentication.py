from fastapi import APIRouter, Depends, HTTPException, status
from ..hashing import Hash
from .. import schemas
from .. import database
from .. import models
from sqlalchemy.orm import Session
from datetime import timedelta
from ..token import create_access_token  # Ensure this is imported correctly

router = APIRouter(tags=['Authentication'])

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Define your expiration time

@router.post('/login')
def login(request: schemas.Login, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()  # Get the first user
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not Hash.verify(user.password, request.password):  # Check password
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, 
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
