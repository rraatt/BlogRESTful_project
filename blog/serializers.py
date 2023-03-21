from rest_framework import serializers

from blog.models import BlogPost


class BlogSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = BlogPost
        fields = '__all__'
