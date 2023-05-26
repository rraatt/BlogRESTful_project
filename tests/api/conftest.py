import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.contrib.auth.models import User

from blog.models import BlogPost, Tag


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user():
    User = get_user_model()
    user = User.objects.create_user(
        username='testuser',
        email='testuser@example.com',
        first_name='first_name',
        last_name='last_name',
        password='password'
    )
    return user

@pytest.fixture
def admin_user():
    """Create and return an admin user"""
    user = User.objects.create_user('admin', password='adminpass')
    user.is_staff = True
    user.is_superuser = True
    user.save()
    return user


@pytest.fixture
def blogs_user():
    user = User.objects.create_user('user', password='pass')
    user.save()
    tag1 = Tag.objects.create(title='tag1')
    tag1.save()
    tag2 = Tag.objects.create(title='tag2')
    tag2.save()
    post1 = BlogPost.objects.create(title='title1', content='Title 1 content', author=user)
    post1.tags.set([tag1])
    post1.save()
    post2 = BlogPost.objects.create(title='title2', content='Title 2 content', author=user)
    post2.tags.set([tag2])
    post2.save()
    return user
