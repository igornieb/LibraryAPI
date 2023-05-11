from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class LibraryUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ("A", "Admin"),
        ("L", "Librarian"),
        ("U", "User"),
    ]
    user_type = models.CharField(max_length=1, choices=USER_TYPE_CHOICES, default="U")

    def __str__(self):
        return f"{self.user_type} {self.username}"



class Book(models.Model):
    isbn = models.CharField(max_length=17)
    title = models.TextField()
    author = models.TextField()
    description = models.TextField()
    published_date = models.DateTimeField()


class BookInstance(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    serial_number = models.CharField(max_length=50)
    condition_description = models.TextField()


class BorrowedBook(models.Model):
    user = models.ForeignKey(LibraryUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(default=timezone.now)
    predicted_return_date = models.DateTimeField(default=timezone.now)
    return_date = models.DateTimeField(default=timezone.now)
