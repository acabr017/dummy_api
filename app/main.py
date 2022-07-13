from fastapi import Body, FastAPI, Depends
from . import models
from .database import engine, get_db
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware

#from .config import Settings


# No longer really necessary since Alembic will create tables for us
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app .add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
#            {"title": "favourite foods", "content": "I like pizza", "id": 2}]

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
async def root():
    return {"message": "Home Page. Successfully deployed from CI/CD pipeline."}
