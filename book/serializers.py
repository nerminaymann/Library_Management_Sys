from rest_framework import serializers
from author.serializers import AuthorSerializer
from .models import Book, Category

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

# class BorrowTransactionSerializer(serializers.ModelSerializer):
#     books = BooksDetailSerializer(many=True)
#     class Meta:
#         model = BorrowTransaction
#         fields = '__all__'
#
# class ReturnTransactionSerializer(serializers.ModelSerializer):
#     borrow_transaction = BorrowTransactionSerializer()
#     class Meta:
#         model = ReturnTransaction
#         fields = '__all__'


