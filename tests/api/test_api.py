from collections import OrderedDict
from datetime import datetime

import jwt
import pytest
from django.conf import settings
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_register_user(client):
    payload = {
        'username': 'test',
        'password': 'Testpass69@',
        'email': 'test@test.com',
        'first_name': 'testname',
        'second_name': 'testsecondname'
    }

    response = client.post('/api/v1/register/', data=payload)

    assert 'access' in response.data
    assert 'refresh' in response.data

    # decode and verify access token
    access_token = response.data['access']
    try:
        decoded_token = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        pytest.fail("Access token has expired")
    except jwt.InvalidTokenError:
        pytest.fail("Access token is invalid")

    # check that the user id in the token matches the registered user id
    assert decoded_token['user_id'] == User.objects.get(username='test').id


@pytest.mark.django_db
def test_auth(user, client):
    response = client.post('/api/v1/token/', data={'username': 'testuser',
                                                   'password': 'password'})

    assert 'access' in response.data
    assert 'refresh' in response.data

    # decode and verify access token
    access_token = response.data['access']
    try:
        decoded_token = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        pytest.fail("Access token has expired")
    except jwt.InvalidTokenError:
        pytest.fail("Access token is invalid")

    # check that the user id in the token matches the registered user id
    assert decoded_token['user_id'] == User.objects.get(username='testuser').id


@pytest.mark.django_db
def test_blogs(blogs_user, client):
    response = client.get('/api/v1/blogs/')

    assert response.status_code == 200
    assert response.data['results'] == [OrderedDict([('title', 'title1'), ('content', 'Title 1 content'),
                                                     ('author',
                                                      OrderedDict([('id', 1), ('first_name', ''), ('last_name', '')])),
                                                     ('tags', [OrderedDict([('id', 1), ('title', 'tag1')])])]),
                                        OrderedDict([('title', 'title2'), ('content', 'Title 2 content'),
                                                     ('author',
                                                      OrderedDict([('id', 1), ('first_name', ''), ('last_name', '')])),
                                                     ('tags', [OrderedDict([('id', 2), ('title', 'tag2')])])])]


@pytest.mark.django_db
def test_blogs_id(blogs_user, client):
    response = client.get('/api/v1/blogs/1/')

    assert response.status_code == 200
    data = response.data.copy()  # create a copy of the data
    del data['time_create']  # delete the key you want to ignore
    del data['time_update']
    assert data == {'id': 1, 'author': 1, 'title': 'title1', 'tags':
        [OrderedDict([('id', 1), ('title', 'tag1')])], 'content': 'Title 1 content', 'comments': []}


@pytest.mark.django_db
def test_blogs_tags(blogs_user, client):
    response = client.get('/api/v1/blogs/?tags=tag1')
    assert response.status_code == 200
    assert response.data == OrderedDict([('count', 1), ('next', None), ('previous', None),
                                         ('results', [OrderedDict([('title', 'title1'), ('content', 'Title 1 content'),
                                                                   ('author', OrderedDict(
                                                                       [('id', 1), ('first_name', ''),
                                                                        ('last_name', '')])),
                                                                   ('tags',
                                                                    [OrderedDict([('id', 1), ('title', 'tag1')])])])])])


@pytest.mark.django_db
def test_blogs_tags(blogs_user, client):
    response = client.get('/api/v1/blogs/?search=title1')
    assert response.status_code == 200
    assert response.data == OrderedDict([('count', 1), ('next', None), ('previous', None),
                                         ('results', [OrderedDict([('title', 'title1'), ('content', 'Title 1 content'),
                                                                   ('author', OrderedDict(
                                                                       [('id', 1), ('first_name', ''),
                                                                        ('last_name', '')])),
                                                                   ('tags',
                                                                    [OrderedDict([('id', 1), ('title', 'tag1')])])])])])


@pytest.mark.django_db
def test_blogs_create(client, user):
    client.force_authenticate(user=user)
    payload = {'title': 'title1', 'content': 'title1 content'}
    response = client.post('/api/v1/blogs/', data=payload)
    assert response.data == {'title': 'title1', 'content': 'title1 content',
                             'author': OrderedDict([('id', 1), ('first_name', 'first_name'),
                                                    ('last_name', 'last_name')]), 'tags': []}


def test_blogs_create(client):
    payload = {'title': 'title1', 'content': 'title1 content'}
    response = client.post('/api/v1/blogs/', data=payload)
    assert response.status_code == 401
