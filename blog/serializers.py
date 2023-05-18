from rest_framework import serializers
from django.contrib.auth.models import User
from blog.models import BlogPost, Comment, Tag, Profile


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for registering employees into the system"""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']


class ProfileSerializer(serializers.ModelSerializer):
    account = AuthorSerializer()

    class Meta:
        model = Profile
        fields = ['account', 'bio']


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    owner = AuthorSerializer()

    def get_replies(self, obj):
        replies = Comment.objects.filter(answered_comment=obj)
        return CommentSerializer(replies, many=True).data

    class Meta:
        model = Comment
        fields = ['id', 'content', 'time_create', 'time_update', 'owner', 'replies']


class BlogDetailedSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)
    tags = TagsSerializer(many=True)

    class Meta:
        model = BlogPost
        fields = ['id', 'author', 'title', 'tags', 'time_create', 'time_update', 'content', 'comments']


class BlogUpdateCreateSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = BlogPost
        fields = '__all__'


class BlogListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    tags = TagsSerializer(many=True)

    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'author', 'tags']
