from rest_framework import serializers
from book.serializers import CategorySerializer, BooksDetailSerializer
from .models import Library

class LibrarySerializer(serializers.ModelSerializer):
    books = BooksDetailSerializer(many=True)
    categories = serializers.SerializerMethodField()

    class Meta:
        model = Library
        fields = ['id', 'name', 'location', 'books', 'categories']

    def get_categories(self, obj):
        # Get unique categories for each library
        categories = obj.books.values_list('category__name', flat=True).distinct()
        return list(categories)
