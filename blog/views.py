from django.shortcuts import render
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from blog.models import BlogPost
from blog.permissions import IsOwnerOrReadOnly, IsOwnerOrAdmin
from blog.serializers import BlogSerializer


# Create your views here.

class BlogAPIListPagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'page_size'
    max_page_size = 100


class BlogAPIList(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogSerializer
    pagination_class = BlogAPIListPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)


class BlogAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class BlogAPIDestroyView(generics.RetrieveDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogSerializer
    permission_classes = (IsOwnerOrAdmin,)
