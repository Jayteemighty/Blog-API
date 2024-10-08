from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from user.api import router as user_router
from blog.api import router as blog_router

api = NinjaAPI()

api.add_router("/user/", user_router)
api.add_router("/blog/", blog_router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", api.urls),
]
