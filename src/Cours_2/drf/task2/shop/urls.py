from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .viewsets import AuthorViewSet, BookViewSet

router = DefaultRouter()
router.register(r"books", BookViewSet)
router.register(r"authors", AuthorViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
]
