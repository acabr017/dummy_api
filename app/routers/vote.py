from email.policy import HTTP
from .. import models, schemas, utils, database, oauth2
from sqlalchemy.orm import Session
from fastapi import Body, status, HTTPException, Depends, APIRouter
from ..database import get_db


router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db),
         current_user: int = Depends(oauth2.get_current_user)):
    # Let's check to see if the post exists:
    voted_post = db.query(models.Post).filter(
        models.Post.id == vote.post_id).first()
    if not voted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            details=f"Post with ID {vote.post_id} does not exist.")

    # This will query the Vote table and see if there is already an entry for that vote Id and user ID
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    # This is the result of running the above query
    found_vote = vote_query.first()
    # The vote direction should be either 0 or 1. If it's 1, the user wants to create the vote.
    if (vote.dir == 1):
        # If there was already a found vote, then the user can't like it again.
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"User {current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added vote."}
    # If the vote direction isn't 1 (should be 0), then the user wants to delete the vote.
    else:
        # If there wasn't a vote, the user can't delete it.
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "Successfully deleted vote."}
