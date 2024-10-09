from django.shortcuts import get_object_or_404
from rest_framework import serializers
from author.serializers import AuthorSerializer
from .models import Book, Category, Transaction
from django.utils import timezone

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
    book = serializers.StringRelatedField(read_only=True)
    library = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Transaction
        fields = ['id', 'user', 'book', 'library', 'borrow_date', 'return_date', 'returned', 'actual_return_date']
        read_only_fields = ['user', 'book', 'library', 'return_date', 'returned', 'actual_return_date']

    def create(self, validated_data):
        # Automatically calculate the return date (30 days from borrow_date)
        borrow_date = validated_data.get('borrow_date', timezone.now())
        return_date = borrow_date + timezone.timedelta(days=30)
        validated_data['return_date'] = return_date
        return super().create(validated_data)

class ReturnTransactionSerializer(serializers.ModelSerializer):
    book = serializers.IntegerField()
    class Meta:
        model = Transaction
        fields = ['book']
        read_only_fields = ['returned','borrow_date','actual_return_date']

    def validate(self, attrs):
        user = self.context['request'].user
        book_id = attrs['book']
        # Check for an active transaction with this book and user
        try:
            transaction = Transaction.objects.get(book__id=book_id, user=user, returned=False)
        except Transaction.DoesNotExist:
            raise serializers.ValidationError(
                {"detail": "No active transaction found for this book."}
            )
        attrs['transaction'] = transaction
        return attrs