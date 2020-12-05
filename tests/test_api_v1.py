"""
MIT License
Copyright (c) 2020 Andy Zhou
"""
import json
from flask import url_for
from flog.models import User
from tests.helpers import register, get_api_v1_headers
from flog import fakes as fake

def test_api_index(client):
    response = client.get(url_for('api_v1.index'))
    data = response.get_json()
    assert data['api_version'] == '1.0'


def test_no_auth(client):
    response = client.get(url_for('api_v1.post', post_id=1))
    assert response.status_code == 401


def test_posts(client):
    register(email='user@example.com', password='1234',
             username='user', client=client)
    response = client.post(
        url_for('api_v1.new_post'),
        headers=get_api_v1_headers('user', '1234'),
        data=json.dumps(
            {'content': '<p>body of the post</p>',
             'title': 'hello',
             'private': False}
        )
    )
    assert response.status_code == 200
    data = response.get_json()
    post_id = data.get('id')
    assert post_id is not None
    assert data.get('content') == '<p>body of the post</p>'
    assert data.get('title') == 'hello'
    assert data.get('private') is False

    response = client.get(
        url_for('api_v1.post', post_id=post_id),
        headers=get_api_v1_headers('user', '1234')
    )
    data = response.get_json()
    assert isinstance(data['author'], dict)
    assert data['author']['username'] == 'user'

    data = {
        'title': 'a new title',
        'content': 'the new content',
        'private': True
    }
    response = client.put(
        url_for('api_v1.post', post_id=post_id),
        json=data,
        headers=get_api_v1_headers('user', '1234')
    )
    assert response.status_code == 204

    response = client.get(
        url_for('api_v1.post', post_id=post_id),
        headers=get_api_v1_headers('user', '1234')
    )
    assert response.status_code == 200
    assert response.get_json().get('content') == data['content']

    response = client.patch(
        url_for('api_v1.post', post_id=post_id),
        headers=get_api_v1_headers('user', '1234')
    )
    assert response.status_code == 204

    response = client.get(
        url_for('api_v1.post', post_id=post_id),
        headers=get_api_v1_headers('user', '1234')
    )
    assert response.get_json()['private'] is False

    response = client.delete(
        url_for('api_v1.post', post_id=post_id),
        headers=get_api_v1_headers('user', '1234')
    )
    assert response.status_code == 204

    response = client.get(
        url_for('api_v1.post', post_id=post_id),
        headers=get_api_v1_headers('user', '1234')
    )
    assert response.status_code == 404


def test_users(client):
    register(email='user@example.com', password='1234',
             username='user', client=client)
    user = User.query.filter_by(username='user').first()
    assert user is not None
    response = client.get(
        url_for('api_v1.user', user_id=user.id),
        headers=get_api_v1_headers('user', '1234')
    )
    data = response.get_json()
    assert data['id'] == user.id
    assert data['username'] == user.username

    # test put method
    user_data = {
        'name': 'Real Name',
        'about_me': 'A test user.',
        'location': 'Shanghai'
    }
    response = client.put(
        url_for('api_v1.user', user_id=user.id),
        json=user_data,
        headers=get_api_v1_headers('user', '1234')
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == user_data['name']
    assert data['about_me'] == user_data['about_me']
    assert data['location'] == user_data['location']

    # test delete method
    response = client.delete(
        url_for('api_v1.user', user_id=user.id),
        headers=get_api_v1_headers('user', '1234')
    )
    assert response.status_code == 200
    assert response.get_data(as_text=True) == f'User id {user.id} deleted.'
    assert User.query.get(user.id) is None


def test_notifications(client):
    register(email='user@example.com', password='1234',
             username='user', client=client)
    fake.notifications(10)
    response = client.get(
        url_for('api_v1.notification'),
        headers=get_api_v1_headers('user', '1234')
    )
    data = response.get_json()
    assert data.get('unread_num') == 10
    assert isinstance(data.get('unread_items'), list)
    assert isinstance(data.get('unread_items')[1], dict)
