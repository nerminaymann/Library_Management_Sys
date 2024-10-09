from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_datetime
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, serializers
from rest_framework.response import Response
from django.utils import timezone
from library.models import Library
from .models import Book,Transaction
from .serializers import BooksDetailSerializer, BorrowTransactionSerializer,ReturnTransactionSerializer
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

class BorrowBookView(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = BorrowTransactionSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        book_id = self.kwargs['book_id']
        # library_id = request.data.get('library')
        borrow_date_str = request.data.get('borrow_date')
        user = request.user
        if borrow_date_str:
            try:
                # Parse borrow_date string into a datetime object
                borrow_date = parse_datetime(borrow_date_str)
                if borrow_date is None:
                    raise ValueError("Invalid date format")
            except ValueError:
                return Response({"error": "Invalid borrow_date format. Use ISO 8601 format."},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            borrow_date = timezone.now()
        book = get_object_or_404(Book, id=book_id)
        # library = get_object_or_404(Library, id=library_id)
        # Check if the book is available
        if not book.is_available:
            return Response({"error": "This book is not available"},
                            status=status.HTTP_400_BAD_REQUEST)
        # Check if the user already has an active transaction for this book
        if Transaction.objects.filter(user=user, book=book, returned=False).exists():
            return Response({"error": "You already have this book borrowed and haven't returned it yet."},
                            status=status.HTTP_400_BAD_REQUEST)
        # Calculate maximum return date after 30 days
        borrow_period = borrow_date + timezone.timedelta(days=30)
        transaction = Transaction.objects.create(
            user=user,
            book=book,
            library=book.library,
            borrow_date=borrow_date,
            return_date=borrow_period,
            returned=False
        )
        book.is_available = False
        book.save()
        # Trigger Celery task to send a confirmation email (if implemented)
        send_borrow_confirmation_email.delay(user.email, book.title)
        response_data = {
            'message': 'Book borrowed successfully!',
            'transaction': BorrowTransactionSerializer(transaction).data
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

class ReturnBookView(generics.UpdateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = ReturnTransactionSerializer
    # lookup_url_kwarg = 'transaction_id'
    permission_classes = [IsAuthenticated]

    def put(self, request, book_id, *args, **kwargs):
        serializer = self.get_serializer(data={"book": book_id})
        serializer.is_valid(raise_exception=True)
        # Retrieve the validated transaction instance
        transaction = serializer.validated_data['transaction']
        if transaction.returned:
            return Response({"error": "This book has already been returned."}, status=status.HTTP_400_BAD_REQUEST)
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
        return Response({
            "message": f'Book "{transaction.book.title}" returned successfully!'
        }, status=status.HTTP_200_OK)