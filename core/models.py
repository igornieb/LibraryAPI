import os

from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone

from core.validators import ISBNValidator


class LibraryUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ("S", "Staff"),
        ("U", "User"),
    ]
    user_type = models.CharField(max_length=1, choices=USER_TYPE_CHOICES, default="U")

    def __str__(self):
        return f"{self.user_type} {self.username}"


class Author(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Book(models.Model):
    def upload_to(self, filename):
        return f'uploads/{filename}'

    created_by = models.ForeignKey(LibraryUser, on_delete=models.DO_NOTHING)
    authors = models.ManyToManyField('Author')
    isbn = models.CharField(max_length=10, unique=True, validators=[ISBNValidator])
    title = models.TextField()
    description = models.TextField()
    cover = models.ImageField(upload_to=upload_to, default="uploads/default.png", validators=[FileExtensionValidator(['jpeg', 'jpg', 'png', 'webp'])])
    published_date = models.DateTimeField()
