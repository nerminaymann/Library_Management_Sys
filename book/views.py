from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, serializers
from rest_framework.response import Response
from django.utils import timezone
from .models import Book,BorrowTransaction
from .serializers import BooksDetailSerializer, BorrowTransactionSerializer
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

class BorrowBookView(generics.ListCreateAPIView):
    queryset = BorrowTransaction.objects.all()
    serializer_class = BorrowTransactionSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        book_id = self.kwargs['book_id']
        book = get_object_or_404(Book, id=book_id)

        if not book.is_available:
            return Response({"error": "This book is not available"}, status=status.HTTP_400_BAD_REQUEST)

        borrow_period = timezone.now() + timezone.timedelta(days=30)
        user = self.request.user

        serializer.save(
            user=user,
            book=book,
            library=book.library,
            return_date=borrow_period
        )
        book.available = False
        book.save()

        # Trigger the Celery task to send a confirmation email
        send_borrow_confirmation_email.delay(user.email, book.title)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        transaction = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({
            'message': 'Book borrowed successfully!',
            'transaction': BorrowTransactionSerializer(transaction).data
        }, status=status.HTTP_201_CREATED, headers=headers)

class ReturnBookView(generics.UpdateAPIView):
    queryset = BorrowTransaction.objects.all()
    serializer_class = BorrowTransactionSerializer
    lookup_url_kwarg = 'transaction_id'

    def perform_update(self, serializer):
        transaction = self.get_object()
        if transaction.returned:
            raise serializers.ValidationError("This book has already been returned")
        transaction.returned = True
        transaction.save()

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