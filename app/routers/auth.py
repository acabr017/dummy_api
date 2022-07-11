from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=schemas.Token)
# If we use OAuth2PasswordRequestForm it doesn't have the user sign in using "email"
# It calls it "username". So we have to change our search in the database from .email to .username
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    # Grab the user by checking User table for the email.
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()
    # If that user email isn't in the table, raises a 404 error
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    # Checks that the provided password, when hashed, matches the stored password. If not, raises 404.
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # Need to create the JWT Token
    # What we put into the token is up to us
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "Bearer"}
