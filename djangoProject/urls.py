"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path

from blog.views import BlogAPIList, BlogAPIRetrieve, UserRegistrationView, ProfileView, BlogAPIUpdateDestroyView, \
    TagsView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView, TokenRefreshView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/blogs/', BlogAPIList.as_view()),
    path('api/v1/blogs/<int:pk>/', BlogAPIRetrieve.as_view()),
    path('api/v1/blogs/<int:pk>/edit/', BlogAPIUpdateDestroyView.as_view()),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/v1/register/', UserRegistrationView.as_view(), name='registration'),
    path('api/v1/profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('api/v1/tags/', TagsView.as_view(), name='tags')
]
