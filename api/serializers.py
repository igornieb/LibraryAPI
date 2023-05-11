from rest_framework import serializers
from core.models import *


class LibraryUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryUser
        fields = ["username", "first_name", "last_name", "user_type"]


class AuthorSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = Author
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)
    created_by = LibraryUserSerializer(many=False)

    class Meta:
        model = Book
        fields = "__all__"


class BookCreateSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=False, partial=True)
    created_by = serializers.CharField()

    class Meta:
        model = Book
        fields = ["authors", "created_by", "isbn", "title", "description", "published_date"]

    def create(self, validated_data):
        try:
            owner = LibraryUser.objects.get(username=validated_data['created_by'], user_type="S")
        except LibraryUser.DoesNotExist:
            raise serializers.ValidationError({"detail": "LibraryUser does not exist or isn't set as staff"})
        book = Book.objects.create(created_by=owner, title=validated_data['title'], description=validated_data['description'], isbn=validated_data['isbn'], published_date=validated_data['published_date'] )
        authors_data = validated_data.pop('authors')
        for author in authors_data:
            if author.get('id'):
                try:
                    book.authors.add(Author.objects.get(id=author.get("id"), first_name=author.get("first_name"), last_name=author.get('last_name')))
                except Author.DoesNotExist:
                    raise serializers.ValidationError({"detail": "author does not exist"})
            else:
                book.authors.add(Author.objects.create(first_name=author.get("first_name"), last_name=author.get('last_name')))
        return book


class BookUpdateSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)

    class Meta:
        model = Book
        fields = ["authors", "isbn", "title", "description", "published_date"]
