from rest_framework import serializers
from core.models import *


class LibraryUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryUser
        fields = ["first_name", "last_name", "user_type"]


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["first_name", "last_name"]


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)
    created_by = LibraryUserSerializer(many=False)

    class Meta:
        model = Book
        fields = "__all__"
