from django.urls import path

from user.urls import app_name
from .views import BookListView

app_name = 'book'
urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),
]
