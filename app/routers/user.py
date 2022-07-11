from .. import models, schemas, utils
from sqlalchemy.orm import Session
from fastapi import Body, status, HTTPException, Depends, APIRouter
from ..database import get_db

router = APIRouter(prefix="/users", tags=['Users'])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    # first we have to hash the password (found int user.password)
    # then we override the value stored in user
    user.password = utils.hash(user.password)
    # Unpacks the dictionary to fill out table
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")
    return user
