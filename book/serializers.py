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
    books = BooksDetailSerializer(many=True)
    class Meta:
        model = BorrowTransaction
        fields = '__all__'

