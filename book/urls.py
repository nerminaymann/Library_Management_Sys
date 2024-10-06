from django.urls import path

from user.urls import app_name
from .views import BookListView, BorrowBookView, ReturnBookView

app_name = 'book'
urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),
    path('borrow/<int:book_id>/', BorrowBookView.as_view(), name='borrow-book'),
    path('return/<int:transaction_id>/', ReturnBookView.as_view(), name='return-book'),
]
