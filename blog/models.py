from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy
from uuid import uuid4

class BlogPost(models.Model):
    '''Model representing a blog post.'''
    
    id = models.UUIDField(default=uuid4, primary_key=True)
    title = models.CharField(max_length=255, null=False)
    content = models.TextField(null=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
