from rest_framework import serializers
from post.models import Post


class PostSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'image', 'description', 'author', 'created_at', 'updated_at')

    def create(self, validated_data):
        return Post.objects.create(**validated_data)