from rest_framework import serializers
from .models import Book, Category, BorrowTransaction, ReturnTransaction
from author.serializers import AuthorSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    category = CategorySerializer()
    class Meta:
        model = Book
        fields = [ 'title', 'author', 'category']

class BorrowTransactionSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True)

    class Meta:
        model = BorrowTransaction
        fields = '__all__'

class ReturnTransactionSerializer(serializers.ModelSerializer):
    borrow_transaction = BorrowTransactionSerializer()

    class Meta:
        model = ReturnTransaction
        fields = '__all__'


