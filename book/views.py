
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from .models import Book
from .serializers import BooksDetailSerializer
from .filters import BookFilter

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BooksDetailSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter
