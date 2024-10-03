from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.response import Response
from .filters import AuthorFilter
from .models import Author
from .serializers import AuthorWithBookCountSerializer,AuthorWithBooksSerializer

class AuthorListView(generics.ListAPIView):
    filter_backends = [DjangoFilterBackend]
    filterset_class = AuthorFilter
    serializer_class = AuthorWithBookCountSerializer

    def get_queryset(self):
        queryset = Author.objects.all()
        library_filter = self.request.query_params.get('library', None)
        category_filter = self.request.query_params.get('category', None)

        if library_filter:
            queryset = queryset.filter(books__library__name__icontains=library_filter)
        if category_filter:
            queryset = queryset.filter(books__category__name__icontains=library_filter)

        queryset = queryset.annotate(book_count=Count('books', filter=Q(
            books__library__name__icontains=library_filter if library_filter else '',
            books__category__name__icontains=category_filter if category_filter else ''
        )))
        return queryset

class AuthorDetailView(generics.RetrieveAPIView):
    serializer_class = AuthorWithBooksSerializer
    queryset = Author.objects.all()
    def get_author(self,request,pk):
        author = get_object_or_404(Author, id=pk)
        serializer = AuthorWithBooksSerializer(author)
        return Response(data = serializer.data,status=status.HTTP_200_OK)
