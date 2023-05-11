from django.shortcuts import render
from core.models import *
from api.serializers import BookSerializer
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView
from api.permissions import IsStaff

class BookList(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def create(self, request, *args, **kwargs):
        pass

# Create your views here.
