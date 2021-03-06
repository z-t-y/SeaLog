"""
MIT License
Copyright (c) 2020 Andy Zhou
"""
from random import randint
from faker import Faker
from flog.models import Post, User
from flog.utils import lower_username
from .helpers import generate_post, login

fake = Faker()


def test_admin_edit_user_profile(client):
    login(client)
    response = client.get("/admin/user/all/")
    assert response.status_code == 200
    user_id = randint(2, 5)
    data = {
        "email": fake.email(),
        "username": lower_username(fake.name()),
        "confirmed": bool(randint(0, 1)),
        "role": 1,
        "name": fake.name(),
        "location": fake.address(),
        "about_me": fake.text(),
        "custom_avatar_url": "https://example.com/test.png"
    }
    response = client.post(
        f"/admin/user/{user_id}/profile/edit/", data=data, follow_redirects=True
    )
    response_data = response.get_data(as_text=True)
    assert data["email"] in response_data
    assert data["username"] in response_data
    assert data["about_me"] in response_data
    assert data["location"] in response_data
    assert data["custom_avatar_url"] in response_data

    data["username"] = User.query.get(1).username
    data["email"] = User.query.get(1).email
    response = client.post(
        f"/admin/user/{user_id}/profile/edit/", data=data, follow_redirects=True
    )
    data = response.get_data(as_text=True)
    assert "already registered" in data


def test_user_delete(client):
    login(client)
    user_id = randint(2, 5)
    response = client.post(
        f"/admin/users/delete/{user_id}/", follow_redirects=True
    )
    assert response.status_code == 200
    assert User.query.get(user_id) is None
