from django.db.models import Count, Q
from rest_framework import generics
from .models import Author
from book.models import Book
from .serializers import AuthorWithBookCountSerializer,AuthorSerializer

class AuthorListView(generics.ListAPIView):
    serializer_class = AuthorWithBookCountSerializer

    def get_queryset(self):
        library_name = self.request.query_params.get('library', None)
        category_name = self.request.query_params.get('category', None)
        author_name = self.request.query_params.get('author_name', None)
        books = Book.objects.all()

        if author_name:
            books = books.filter(name__icontains=author_name)
        # Apply filtering by library, if provided
        if library_name:
            books = books.filter(library__name__icontains=library_name)

        # Apply filtering by category, if provided
        if category_name:
            books = books.filter(category__name__icontains=category_name)

        # Get authors with the filtered book counts
        queryset = Author.objects.annotate(
            book_count=Count('books', filter=Q(books__in=books))
        ).filter(book_count__gt=0)  # Only include authors with at least one book matching the filters

        return queryset


