"""
MIT License
Copyright (c) 2020 Andy Zhou
"""
from flog import db
from flog.models import Post, User, Notification, Group


def test_password_setter(client):
    u = User()
    u.set_password("hello")
    assert u.password_hash is not None


def test_password_verification(client):
    u = User()
    u.set_password("hello")
    assert u.verify_password("hello")
    assert not u.verify_password("bye")


def test_password_salts_are_random(client):
    u1 = User()
    u2 = User()
    u1.set_password("hello")
    u2.set_password("hello")
    assert u1.password_hash != u2.password_hash


def test_confirmation_token(client):
    u = User(email="test@example.com")
    token = u.generate_confirmation_token()
    assert u.confirm(token)


def test_collect(client):
    user = User()
    post = Post()
    user.collect(post)
    assert user.is_collecting(post)


def test_follow(client):
    user1 = User()
    user2 = User()
    user1.follow(user2)
    assert user1.is_following(user2)


def test_notification(client):
    user = User()
    notification = Notification(message="Hello World", receiver=user)
    db.session.add(notification)
    db.session.commit()
    assert notification in user.notifications


def test_group(client):
    user = User()
    group = Group()
    user.join_group(group)
    assert user.in_group(group)
