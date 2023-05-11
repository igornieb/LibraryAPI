from django.urls import resolve, reverse
from rest_framework.test import APITestCase
from api.views import *
from api.urls import TokenObtainPairView, TokenRefreshView
from rest_framework.authtoken.models import Token
from api.serializers import *


class UrlsTest(APITestCase):
    # Tests if all api urls are resolved correctly
    def test_token_url(self):
        url = reverse('token-obtain-pair')
        self.assertEqual(resolve(url).func.view_class, TokenObtainPairView)

    def test_token_refresh_url(self):
        url = reverse('token-refresh')
        self.assertEqual(resolve(url).func.view_class, TokenRefreshView)

    def test_register_url(self):
        url = reverse('register-user')
        self.assertEqual(resolve(url).func.view_class, RegisterLibraryUser)

    def test_books_url(self):
        url = reverse('book-list')
        self.assertEqual(resolve(url).func.view_class, BookList)

    def test_book_id_url(self):
        url = reverse('book-details', kwargs={'isbn': "9788390021"})
        self.assertEqual(resolve(url).func.view_class, BookDetails)


class BookListTest(APITestCase):
    url = reverse('book-list')

    def setUp(self):
        self.user = LibraryUser.objects.create_user(username='user', password='user', is_superuser=False, user_type="S")
        self.staff = LibraryUser.objects.create_user(username='staff', password='admin', is_superuser=True,
                                                     user_type="S")
        self.AMick = Author.objects.create(first_name="Adam", last_name="Mickiewicz")
        self.JSlow = Author.objects.create(first_name="Juliusz", last_name="Slowacki")
        self.token_staff = Token.objects.create(user=self.staff)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_staff.key)

    def test_method_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_method_post_unauthenticeted(self):
        self.client.force_authenticate(user=None, token=None)
        query = {
            "authors": [
                {
                    "id": self.AMick.id,
                    "first_name": self.AMick.first_name,
                    "last_name": self.AMick.last_name,
                },
                {
                    "first_name": "test_name",
                    "last_name": "test_lastname",
                }
            ],
            "created_by": self.staff.username,
            "title": "title",
            "description": "description",
            "isbn": "9788390021",
            "published_date": "2023-05-11T08:42:07Z"
        }
        response = self.client.post(self.url, query, format='json')
        # book was not created, response code matches expectations
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEquals(Book.objects.filter(isbn="9788390021").exists(), True)

    def test_method_post_authenticated_valid(self):
        query = {
            "authors": [
                {
                    "id": self.AMick.id,
                    "first_name": self.AMick.first_name,
                    "last_name": self.AMick.last_name,
                },
                {
                    "first_name": "test_name",
                    "last_name": "test_lastname",
                }
            ],
            "created_by": self.staff.username,
            "title": "title",
            "description": "description",
            "isbn": "9788390021",
            "published_date": "2023-05-11T08:42:07Z"
        }
        response = self.client.post(self.url, query, format='json')
        # book was created, response code matches expectations
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(Book.objects.filter(isbn="9788390021").exists(), True)
        self.assertEqual(response.data, BookSerializer(Book.objects.get(isbn="9788390021")).data)
        query['authors'] = [
            {
                "id": self.AMick.id,
                "first_name": self.AMick.first_name,
                "last_name": self.AMick.last_name,
            }]
        query['isbn'] = "007462542X"
        response = self.client.post(self.url, query, format='json')
        # book was created, response code and data matches expectations
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(Book.objects.filter(isbn="007462542X").exists(), True)
        self.assertEqual(response.data, BookSerializer(Book.objects.get(isbn="007462542X")).data)

    def test_method_post_authenticated_invalid(self):
        # wrong created_by (user doesn't exist)
        query_createdby = {
            "authors": [
                {
                    "id": self.AMick.id,
                    "first_name": self.AMick.first_name,
                    "last_name": self.AMick.last_name,
                }
            ],
            "created_by": "igorniebylski",
            "title": "title",
            "description": "description",
            "isbn": "9788390021",
            "published_date": "2023-05-11T08:42:07Z"
        }
        response = self.client.post(self.url, query_createdby, format='json')
        # got error response code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # record wasn't created
        self.assertEquals(Book.objects.filter(isbn="9788390022").exists(), False)

        # wrong isbn, correct username
        query_isbn = query_createdby
        query_isbn['created_by'] = self.staff.username
        query_isbn['isbn'] = "97883900"
        response = self.client.post(self.url, query_isbn, format='json')
        # record wasn't created
        self.assertEquals(Book.objects.filter(isbn="97883900").exists(), False)
        # got error response code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class BookDetailsTest(APITestCase):
    def setUp(self):
        self.not_owner = LibraryUser.objects.create_user(username='not_owner', user_type="S", is_superuser=True)
        self.owner = LibraryUser.objects.create_user(username='staff', user_type="S")
        self.AMick = Author.objects.create(first_name="Adam", last_name="Mickiewicz")
        JSlow = Author.objects.create(first_name="Juliusz", last_name="Slowacki")
        self.book = Book.objects.create(created_by=self.owner, title='dziady', description=" ", isbn="9788390021")
        self.book.authors.add(self.AMick, JSlow)
        self.book.save()
        self.url = reverse('book-details', kwargs={'isbn': self.book.isbn})
        self.token = Token.objects.create(user=self.owner)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_method_get(self):
        response = self.client.get(self.url)
        # correct response code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # correct response data
        self.assertEqual(response.data, BookSerializer(self.book).data)

    def test_method_patch_valid_authentiated_authorized(self):
        query = {
            "authors": [
                {
                    "id": self.AMick.id,
                    "first_name": self.AMick.first_name,
                    "last_name": self.AMick.last_name,
                },
                {
                    "first_name": "test_name",
                    "last_name": "test_lastname",
                }
            ],
            "title": "title",
            "description": "description",
            "isbn": "007462542X",
            "published_date": "2023-04-11T08:42:07Z"
        }

        response = self.client.patch(self.url, query, format='json')
        # correct response code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book = Book.objects.get(isbn="007462542X")
        # correct response data
        self.assertEqual(response.data, BookSerializer(self.book).data)
        # new author got saved
        self.assertEqual(self.book.authors.filter(id=self.AMick.id).exists(), True)
        # old author got erased
        self.assertEqual(self.book.authors.filter(first_name="Juliusz", last_name="Slowacki").exists(), False)
        # new author got saved
        self.assertEqual(self.book.authors.filter(first_name="test_name").exists(), True)
        # isbn got updated
        self.assertEqual(self.book.isbn, "007462542X")

    def test_method_patch_valid_authentiated_unauthorized(self):
        # valid data
        query = {
            "authors": [
                {
                    "id": self.AMick.id,
                    "first_name": self.AMick.first_name,
                    "last_name": self.AMick.last_name,
                },
                {
                    "first_name": "test_name",
                    "last_name": "test_lastname",
                }
            ],
            "title": "title",
            "description": "description",
            "isbn": "9781234567",
            "published_date": "2023-04-11T08:42:07Z"
        }
        self.token = Token.objects.create(user=self.not_owner)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.patch(self.url, query, format='json')
        # got error response code
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # new author didn't get saved
        self.assertNotEquals(self.book.authors.filter(first_name="test_name").exists(), True)
        # isbn didnt get updated
        self.assertNotEquals(self.book.isbn, "9781234567")

    def test_method_patch_valid_authentiated_authorized_invalid_data(self):
        # query with incorrect isbn
        query = {
            "authors": [
                {
                    "id": "999999999",
                    "first_name": "TEST",
                    "last_name": "TESTOWY"
                }
            ],
            "isbn": "9781234568",
            "title": "TEST2",
            "description": "TEST22",
            "published_date": "2023-05-11T08:42:07Z"
        }

        response = self.client.patch(self.url, query, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # isbn did not change
        self.assertEqual(self.book.isbn, "9788390021")
        # authors did not change
        self.assertEqual(self.book.authors.filter(id=self.AMick.id).exists(), True)
        self.assertEqual(self.book.authors.filter(first_name="Juliusz").exists(), True)
        self.assertEqual(self.book.authors.count(), 2)
        self.assertEqual(self.book.authors.filter(first_name="TEST2").exists(), False)

        # isbn did not change
        self.assertEqual(Book.objects.filter(isbn="9781234567").exists(), False)
