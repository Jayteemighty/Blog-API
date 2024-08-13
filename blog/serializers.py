from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    '''Serializer to manage Post objects.'''

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'created_at', 'updated_at']
        read_only_fields = ['author', 'created_at', 'updated_at']

    def create(self, validated_data):
        '''Create a new Post object.'''
        user = self.context['request'].user
        validated_data['author'] = user
        return super().create(validated_data)
