from datetime import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from core.models import *


class LibraryUserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # creates testuser User
        LibraryUser.objects.create(username='testuser', first_name="TestName", last_name="LastName")
        LibraryUser.objects.create(username='testuser1', first_name="TestName1", last_name="LastName1", user_type="S")

    def test_user_creation(self):
        # tests if user exists
        user1 = LibraryUser.objects.filter(username='testuser')
        self.assertEqual(True, user1.exists())
        self.assertEqual(user1.first().username, 'testuser')
        self.assertEqual(user1.first().first_name, 'TestName')
        self.assertEqual(user1.first().last_name, 'LastName')

    def test_user_type(self):
        # tests if default user_type is set correctly
        user1 = LibraryUser.objects.get(username='testuser')
        user2 = LibraryUser.objects.get(username='testuser1')

        self.assertEqual("S", user2.user_type)
        self.assertEqual("U", user1.user_type)

    def test_str_representation(self):
        # tests string representation of Model
        user = LibraryUser.objects.get(username='testuser')
        expected_object_name = f"{user.user_type} {user.username}"
        self.assertEqual(str(user), expected_object_name)


class AuthorTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # creates Author
        Author.objects.create(first_name="Adam", last_name="Mickiewicz")

    def test_user_creation(self):
        # tests if user exists
        author = Author.objects.filter(first_name="Adam", last_name="Mickiewicz")
        self.assertEqual(True, author.exists())

    def test_str_representation(self):
        author = Author.objects.get(first_name="Adam", last_name="Mickiewicz")
        self.assertEqual(f"{author.first_name} {author.last_name}", str(author))


class BookModelTest(TestCase):
    @classmethod
    def setUpTestData(self):
        self.AMick = Author.objects.create(first_name="Adam", last_name="Mickiewicz")
        self.JSlow = Author.objects.create(first_name="Juliusz", last_name="Slowacki")
        self.user = LibraryUser.objects.create(username='testuser')

    def test_str_representation(self):
        book = Book(created_by=self.user, title="1", description="1", isbn="9781234567", published_date=datetime.now())
        self.assertEqual(f"{book.title} {book.isbn}", str(book))

    def test_isbn_validation(self):
        # test validator
        valid_isbn = ["0545010225", "9781234567", "9788390021"]
        invalid_isbn = ["0-545-01022-5", "123-456-888", '8781234567', "9788390022"]
        for sn in valid_isbn:
            book = Book(created_by=self.user, title="1", description="1", isbn=sn, published_date=datetime.now())
            book.full_clean()
        with self.assertRaises(ValidationError):
            for sn in invalid_isbn:
                tier = Book(isbn=sn)
                tier.full_clean()

    def test_multiple_authors(self):
        book = Book.objects.create(created_by=self.user, title="1", description="1", isbn="9788390021", published_date=datetime.now())
        book.authors.add(self.AMick, self.JSlow)
        self.assertEqual(book.authors.contains(self.JSlow), True)
        self.assertEqual(book.authors.contains(self.AMick), True)
        self.assertEqual(book.authors.count(), 2)

