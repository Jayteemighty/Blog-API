from ninja import Router
from .models import BlogPost
from .serializers import BlogPostSchema, BlogPostCreateSchema
from typing import List

router = Router()

from ninja.pagination import paginate
from django.db.models import Q

@router.get("/posts", response=List[BlogPostSchema])
@paginate
def list_posts(request, q: str = None):
    if q:
        return BlogPost.objects.filter(Q(title__icontains=q) | Q(content__icontains=q))
    return BlogPost.objects.all()

@router.post("/posts", response=BlogPostSchema)
def create_post(request, payload: BlogPostCreateSchema):
    post = BlogPost.objects.create(**payload.dict())
    return post

@router.get("/posts/{post_id}", response=BlogPostSchema)
def get_post(request, post_id: int):
    return BlogPost.objects.get(id=post_id)

@router.put("/posts/{post_id}", response=BlogPostSchema)
def update_post(request, post_id: int, payload: BlogPostCreateSchema):
    post = BlogPost.objects.get(id=post_id)
    for attr, value in payload.dict().items():
        setattr(post, attr, value)
    post.save()
    return post

@router.delete("/posts/{post_id}")
def delete_post(request, post_id: int):
    post = BlogPost.objects.get(id=post_id)
    post.delete()
    return {"success": True}
