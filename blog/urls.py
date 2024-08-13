from django.urls import path
from .views import router as blog_router

urlpatterns = [
    path('blog/', blog_router.urls),
]
