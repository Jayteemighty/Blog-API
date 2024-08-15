from ninja import Router
from .models import BlogPost
from .schemas import BlogPostSchema, BlogPostResponseSchema
from django.shortcuts import get_object_or_404
from typing import List
from uuid import UUID
from ninja.pagination import paginate
from ninja.security import HttpBearer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

router = Router()


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            # Validate the token
            UntypedToken(token)
            return token
        except (InvalidToken, TokenError) as e:
            raise AuthenticationFailed(f"Invalid token: {str(e)}")


@router.post("/posts/", response=BlogPostResponseSchema, auth=AuthBearer())
def create_post(request, payload: BlogPostSchema):
    post = BlogPost.objects.create(**payload.dict())
    return post

@router.get("/posts/{post_id}/", response=BlogPostResponseSchema)
def get_post(request, post_id: UUID):
    post = get_object_or_404(BlogPost, id=post_id)
    return post

@router.put("/posts/{post_id}/", response=BlogPostResponseSchema, auth=AuthBearer())
def update_post(request, post_id: UUID, payload: BlogPostSchema):
    post = get_object_or_404(BlogPost, id=post_id)
    for attr, value in payload.dict().items():
        setattr(post, attr, value)
    post.save()
    return post

@router.delete("/posts/{post_id}/", auth=AuthBearer())
def delete_post(request, post_id: UUID):
    post = get_object_or_404(BlogPost, id=post_id)
    post.delete()
    return {"success": True}

@router.get("/posts/", response=List[BlogPostResponseSchema])
@paginate()
def list_posts(request):
    return BlogPost.objects.all()
