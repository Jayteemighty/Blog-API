from ninja import Router
from .models import BlogPost
from .schemas import BlogPostSchema, BlogPostResponseSchema
from django.shortcuts import get_object_or_404
from typing import List
from ninja.pagination import paginate
from ninja.security import django_auth

router = Router()

@router.post("/posts/", response=BlogPostResponseSchema, auth=django_auth)
def create_post(request, payload: BlogPostSchema):
    post = BlogPost.objects.create(**payload.dict())
    return post

@router.get("/posts/{post_id}/", response=BlogPostResponseSchema)
def get_post(request, post_id: int):
    post = get_object_or_404(BlogPost, id=post_id)
    return post

@router.put("/posts/{post_id}/", response=BlogPostResponseSchema, auth=django_auth)
def update_post(request, post_id: int, payload: BlogPostSchema):
    post = get_object_or_404(BlogPost, id=post_id)
    for attr, value in payload.dict().items():
        setattr(post, attr, value)
    post.save()
    return post

@router.delete("/posts/{post_id}/", auth=django_auth)
def delete_post(request, post_id: int):
    post = get_object_or_404(BlogPost, id=post_id)
    post.delete()
    return {"success": True}

@router.get("/posts/", response=List[BlogPostResponseSchema])
@paginate()
def list_posts(request):
    return BlogPost.objects.all()
