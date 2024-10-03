from django.urls import path
from .views import AuthorListView,AuthorDetailView

app_name = 'author'

urlpatterns = [
    path('authors/', AuthorListView.as_view(), name='author-list'),
    path('author-books/<int:pk>', AuthorDetailView.as_view(), name='author-list-books'),

]
