from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.pagination import BookPagination
from api.serializers import *
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView


class BookList(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookPagination

    def create(self, request, *args, **kwargs):
        if request.user.is_superuser:
            serializer = BookCreateSerializer(data=request.data)
            if serializer.is_valid():
                book = serializer.save()
                return Response(BookSerializer(book).data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class BookDetails(APIView):
    def get_queryset(self):
        try:
            return Book.objects.get(isbn=self.kwargs['isbn'])
        except Book.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        return Response(BookSerializer(self.get_queryset()).data)

    def patch(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.created_by == request.user:
            serializer = BookUpdateSerializer(queryset, data=request.data)
            if serializer.is_valid():
                book = serializer.save()
                return Response(BookSerializer(book).data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

class RegisterLibraryUser(APIView):
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
