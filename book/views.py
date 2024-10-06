
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.response import Response
from django.utils import timezone
from .models import Book,BorrowTransaction
from .serializers import BooksDetailSerializer, BorrowTransactionSerializer
from .filters import BookFilter
from library.tasks import send_borrow_confirmation_email
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser


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

        book = serializer.validated_data['book']
        return_date = serializer.validated_data['return_date']
        user = self.request.user

        transaction = serializer.save(
            user=user,
            borrow_date=timezone.now()
        )

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
            'transaction': BorrowTransactionSerializer(transaction).data
        }, status=status.HTTP_201_CREATED, headers=headers)

