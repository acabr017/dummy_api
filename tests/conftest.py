import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models


# Lines __ - __ are switching out our database connection from our regular, production ready database to
# a testing databse. We will override the connection in the database.py file here so that our tests use
# a different database

# This URL points to the production database. We need a different databse URL for the testing databse.
# SQLALCHEMY_DATABSE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
SQLALCHEMY_DATABSE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABSE_URL)

# Notice that this no longer says SessionLocal, but TestingSessionLocal.
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

# ======================== Database and Client Fixtures ==================


@pytest.fixture
def db_session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
# The idea here is that it will allow us to start over fresh each time, resetting the databse
def client(db_session):
    # If we drop first then create, if sometihng fails we can still see the database state
    # This uses SQLAlchemy to build tables. Could do the same with Alembic, if desired
    # Instead of having it here (which I could do) I moved it to the session fixture to handle
    # all of the database stuff. This will be reserved for handling the client stuff.
    # Base.metadata.drop_all(bind=engine)
    # Base.metadata.create_all(bind=engine)
    def override_get_db():

        try:
            yield db_session
        finally:
            db_session.close()
    # This will swap out the get_db with override_get_db that points to a different database to test in
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


# ======================== User Creation Fixture ==================
@pytest.fixture
def test_user(client):
    user_data = {"email": "testing_fixture@email.com",
                 "password": "password123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def test_user2(client):
    user_data = {"email": "testing_fixture2@email.com",
                 "password": "password123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

# ================= Authentication/Token Creation Fixture ================


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    # This new client will already have the token authorization in it for us.
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


# ================= Post Creation Fixture ================
@pytest.fixture
def test_posts(test_user, test_user2, db_session):
    # Creating fake post data
    posts_data = [
        {
            "title": "First Title",
            "content": "First content",
            "owner_id": test_user['id']
        },
        {
            "title": "Second Title",
            "content": "Second content",
            "owner_id": test_user['id']
        },
        {
            "title": "Third Title",
            "content": "Third content",
            "owner_id": test_user['id']
        },
        {
            "title": "Fourth Title",
            "content": "Fourth content",
            "owner_id": test_user2['id']
        }]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)
    db_session.add_all(posts)
    db_session.commit()
    posts = db_session.query(models.Post).all()

    return posts
