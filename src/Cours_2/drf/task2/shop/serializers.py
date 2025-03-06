from rest_framework.serializers import IntegerField, ModelSerializer, Serializer

from .models import Author, Book


class BookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class ReduceQuantitySerializer(Serializer):
    buy = IntegerField(required=True)


class AuthorSerializer(ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ["id", "first_name", "last_name", "books"]
