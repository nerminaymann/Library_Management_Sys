from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, serializers
from rest_framework.response import Response
from django.utils import timezone

from library.models import Library
from .models import Book,Transaction
from .serializers import BooksDetailSerializer, TransactionSerializer
from .filters import BookFilter
from library.tasks import send_borrow_confirmation_email
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser

User = get_user_model()

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BooksDetailSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter
    permission_classes = [IsAuthenticated]

class BookDetailView(generics.RetrieveAPIView):
    serializer_class = BooksDetailSerializer
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticated]
    def get_book(self,request,pk):
        book = get_object_or_404(Book, id=pk)
        serializer = BooksDetailSerializer(book)
        return Response(data = serializer.data,status=status.HTTP_200_OK)


class BorrowBookView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        book_id = self.kwargs['book_id']
        book = get_object_or_404(Book, id=book_id)
        # library = Library.objects.get(id=book.library_id)
        # library =
        user = self.request.user

        # Check if the user already has an active transaction for this book
        if Transaction.objects.filter(user=user, book=book, returned=False).exists():
            return Response({
                "error": "You already have this book borrowed and haven't returned it yet."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user has borrowed the same book from another library
        # if Transaction.objects.filter(user=user, book=book).exclude(library=book.library).exists():
        if Transaction.objects.filter(user=user, book=book).exists():
            return Response({
                "error": "You cannot borrow the same book."
            }, status=status.HTTP_400_BAD_REQUEST)

        # if Transaction.objects.filter(user=user, book=book).exclude(library=book.library).exists():
        #     return Response({
        #         "error": "You cannot borrow the same book from another library."
        #     }, status=status.HTTP_400_BAD_REQUEST)

        if not book.is_available:
            return Response({"error": "This book is not available"}, status=status.HTTP_400_BAD_REQUEST)

        borrow_period = timezone.now() + timezone.timedelta(days=30)
        user = self.request.user

        transaction = serializer.save(
            user=user,
            book=book,
            library=book.library,
            return_date=borrow_period
        )
        book.available = False
        book.save()

        # Trigger the Celery task to send a confirmation email
        send_borrow_confirmation_email.delay(user.email, book.title)
        return transaction


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        transaction = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({
            'message': 'Book borrowed successfully!',
            'transaction': TransactionSerializer(transaction).data
        }, status=status.HTTP_201_CREATED, headers=headers)

class ReturnBookView(generics.UpdateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    lookup_url_kwarg = 'transaction_id'

    def perform_update(self, serializer):
        transaction = self.get_object()
        if transaction.returned:
            raise serializers.ValidationError("This book has already been returned")
        # Call the return_book logic to mark the transaction as returned
        transaction.return_book()

        # Trigger WebSocket notification
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'book_availability',
            {
                'type': 'book_availability_update',
                'message': f'The book "{transaction.book.title}" is now available!'
            }
        )

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        transaction = self.get_object()

        return Response({
            "message": f'Book "{transaction.book.title}" returned successfully!'
        }, status=status.HTTP_200_OK)