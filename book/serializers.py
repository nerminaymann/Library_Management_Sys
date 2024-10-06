from rest_framework import serializers
from author.serializers import AuthorSerializer
from .models import Book, Category, BorrowTransaction


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class BooksDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    category = CategorySerializer()
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'category']

class BorrowTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowTransaction
        fields = ['id', 'user', 'book', 'library', 'borrow_date', 'return_date', 'returned']
        read_only_fields = ['user', 'borrow_date', 'returned']

