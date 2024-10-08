from rest_framework import serializers
from author.serializers import AuthorSerializer
from .models import Book, Category, Transaction


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

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'user', 'book', 'library', 'borrow_date', 'return_date', 'returned','actual_return_date']
        # read_only_fields = ['user', 'borrow_date', 'returned', 'actual_return_date']

