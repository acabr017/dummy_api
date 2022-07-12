from typing import List
from app import schemas
import pytest

# ================= Getting Posts Tests ================


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    # With this we can perform more validation of the post returns
    # def validate(post: dict):
    #     return schemas.PostOut(**post)
    # posts_map = map(validate, res.json())
    # posts_list = list(posts_map)

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


def test_unautherized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_unautherized_user_get_one_posts(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_post_that_doesnt_exist(authorized_client, test_posts):
    # This number could be anything
    res = authorized_client.get(f"/posts/1234568746516847984798498168498")
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id


# ================= Post Creation Tests ================
@pytest.mark.parametrize("title, content, published", [
    ("title 1", "content 1", True),
    ("title 2", "content 2", False),
    ("title 3", "content 3", True),
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post(
        "/posts/", json={"title": title, "content": content, "published": published})

    created_post = schemas.PostResponse(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']


def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    res = authorized_client.post(
        "/posts/", json={"title": "random title", "content": "random content"})

    created_post = schemas.PostResponse(**res.json())
    assert res.status_code == 201
    assert created_post.title == "random title"
    assert created_post.content == "random content"
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']


def test_unautherized_user_create_posts(client, test_user, test_posts):
    res = client.post(
        "/posts/", json={"title": "random title", "content": "random content"})
    assert res.status_code == 401

# ================= Post Deleting Tests ================


def test_unauthorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(
        f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_authorized_delete_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f"/posts/{test_posts[0].id}")
    assert res.status_code == 204


def test_authorized_delete_post_non_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f"/posts/48554987496874984984")
    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f"/posts/{test_posts[3].id}")
    assert res.status_code == 403


# ================= Post Update Tests ================

def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title (test)",
        "content": "updated content from pytest",
        "id": test_posts[0].id
    }

    res = authorized_client.put(f'/posts/{test_posts[0].id}', json=data)
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']


def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title": "updated title (test)",
        "content": "updated content from pytest",
        "id": test_posts[3].id
    }
    res = authorized_client.put(f'/posts/{test_posts[3].id}', json=data)
    assert res.status_code == 403


def test_unauthorized_user_update_post(client, test_user, test_posts):
    res = client.put(f'/posts/{test_posts[0].id}')
    assert res.status_code == 401


def test_authorized_update_post_non_exist(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title (test)",
        "content": "updated content from pytest",
        "id": test_posts[0].id
    }
    res = authorized_client.put(
        f"/posts/48554987496874984984", json=data)
    assert res.status_code == 404
