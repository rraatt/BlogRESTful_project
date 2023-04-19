from django.db.models import Q
from django.shortcuts import render
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from blog.models import BlogPost
from blog.permissions import IsOwnerOrReadOnly, IsOwnerOrAdmin
from blog.serializers import BlogDetailedSerializer, BlogUpdateCreateSerializer, BlogListSerializer


# Create your views here.

class BlogAPIListPagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'page_size'
    max_page_size = 100


class BlogAPIList(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogListSerializer
    pagination_class = BlogAPIListPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        queryset = super().get_queryset()
        tags = self.request.query_params.getlist('tags')  # Get list of tags from query parameters
        search_query = self.request.query_params.get('search', None)

        # Filter queryset by tags
        if tags:
            queryset = queryset.filter(tags__title__in=tags)

        if search_query:
            queryset = queryset.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query))

        return queryset


class BlogAPIRetrieve(generics.RetrieveAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogDetailedSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class BlogAPIUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogUpdateCreateSerializer
    permission_classes = (IsOwnerOrAdmin,)


