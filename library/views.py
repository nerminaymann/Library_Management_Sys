from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Library
from .serializers import LibrarySerializer

class LibraryListView(generics.ListAPIView):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtering by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(books__category__name__icontains=category)

        # Filtering by author
        author = self.request.query_params.get('author')
        if author:
            queryset = queryset.filter(books__author__name__icontains=author)

        return queryset