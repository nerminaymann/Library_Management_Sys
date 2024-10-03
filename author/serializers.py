from rest_framework import serializers

from book.models import Book
from .models import Author

class BooksOfAuthorSerializer(serializers.ModelSerializer):
    #to avoid circular import
    def get_serializer_class(self):
        from book.serializers import CategorySerializer
        return CategorySerializer
    category = get_serializer_class
    class Meta:
        model = Book
        fields = ['id','title','category']

class AuthorWithBooksSerializer(serializers.ModelSerializer):
    books = BooksOfAuthorSerializer(many=True, read_only=True)
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']

class AuthorWithBookCountSerializer(serializers.ModelSerializer):
    book_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Author
        fields = ['id', 'name', 'book_count']
