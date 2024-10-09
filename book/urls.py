from django.urls import path

from user.urls import app_name
from .views import BookListView, BorrowBookView, ReturnBookView,BookDetailView

app_name = 'book'
urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('borrow/<int:book_id>/', BorrowBookView.as_view(), name='borrow-book'),
    path('return/<int:book_id>', ReturnBookView.as_view(), name='return-book'),
]
