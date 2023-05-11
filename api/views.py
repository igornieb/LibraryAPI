from django.http import Http404
from django.shortcuts import render
from api.pagination import BookPagination
from core.models import *
from api.serializers import BookSerializer
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView
from api.permissions import IsStaff


class BookList(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookPagination

    def create(self, request, *args, **kwargs):
        # if superuser then create
        pass


class BookDetails(RetrieveUpdateAPIView):
    serializer_class = BookSerializer
    lookup_field = 'isbn'
    def get_queryset(self):
        try:
            return Book.objects.filter(isbn=self.kwargs['isbn'])
        except Book.DoesNotExist:
            raise Http404
    def update(self, request, *args, **kwargs):
        # if owner then edit
        pass

# Create your views here.
