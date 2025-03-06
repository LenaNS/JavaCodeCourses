from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer, ReduceQuantitySerializer


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_serializer_class(self):
        if self.action == "buy":
            return ReduceQuantitySerializer
        return super().get_serializer_class()

    def get_queryset(self):
        queryset = super().get_queryset()
        author_id = self.request.query_params.get("author")
        if author_id:
            queryset = queryset.filter(author_id=author_id)
        return queryset

    @action(detail=False, methods=["get"])
    def paginated_books(self, request):
        queryset = self.get_queryset()
        paginated_books = self.paginate_queryset(queryset)
        if paginated_books is None:
            return Response(BookSerializer(queryset, many=True).data)
        serializer = self.get_serializer(paginated_books, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=["post"], url_name="buy")
    def buy(self, request, pk=None):
        book = self.get_object()
        serializer = ReduceQuantitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        buy = serializer.validated_data["buy"]
        try:
            with transaction.atomic():
                book = Book.objects.select_for_update().get(pk=book.pk)
                book.reduce_quantity(buy)
            return Response(BookSerializer(book).data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
