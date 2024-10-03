from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Author
from .serializers import AuthorWithBookCountSerializer,AuthorSerializer
from book.models import Book
class AuthorListView(generics.ListAPIView):
    serializer_class = AuthorWithBookCountSerializer

    def get_queryset(self):
        library_name = self.request.query_params.get('library', None)
        category_name = self.request.query_params.get('category', None)
        author_name = self.request.query_params.get('author_name', None)
        books = Book.objects.all()

        if library_name:
            books = books.filter(library__name__icontains=library_name)
        if category_name:
            books = books.filter(category__name__icontains=category_name)
        if author_name:
            books = books.filter(name__icontains=author_name)

        queryset = Author.objects.annotate(
            book_count=Count('books', filter=Q(books__in=books))
        ).filter(book_count__gt=0)  # Only include authors with at least one book matching the filters
        return queryset

class AuthorDetailView(generics.RetrieveAPIView):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()
    def get_author(self,request,pk):
        author = get_object_or_404(Author, id=pk)
        serializer = AuthorSerializer(author)
        return Response(data = serializer.data,status=status.HTTP_200_OK)
