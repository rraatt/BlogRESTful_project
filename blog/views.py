from django.db.models import Q
from djoser.conf import User
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from blog.models import BlogPost, Profile
from blog.permissions import IsOwnerOrReadOnly, IsOwnerOrAdmin, IsAuthUser
from blog.serializers import BlogDetailedSerializer, BlogUpdateCreateSerializer, BlogListSerializer, \
    UserRegistrationSerializer, ProfileSerializer


class UserRegistrationView(generics.CreateAPIView):
    """Registering employees into the system"""
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            'message': 'User account created successfully',
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        })


class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    permission_classes = [IsAuthUser, ]
    serializer_class = ProfileSerializer


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
