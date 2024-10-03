from django.db.models import Count, Q
from rest_framework import generics
from .models import Author, Book
from .serializers import AuthorWithBookCountSerializer,AuthorSerializer

class AuthorListView(generics.ListAPIView):
    serializer_class = AuthorWithBookCountSerializer

    def get_queryset(self):
        library_id = self.request.query_params.get('library', None)
        category_name = self.request.query_params.get('category', None)
        books = Book.objects.all()

        # Apply filtering by library, if provided
        if library_id:
            books = books.filter(library_id=library_id)

        # Apply filtering by category, if provided
        if category_name:
            books = books.filter(category__name__icontains=category_name)

        # Get authors with the filtered book counts
        queryset = Author.objects.annotate(
            book_count=Count('books', filter=Q(books__in=books))
        ).filter(book_count__gt=0)  # Only include authors with at least one book matching the filters

        return queryset

