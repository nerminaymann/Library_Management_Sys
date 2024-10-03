from django.urls import path
from .views import AuthorListView

app_name = 'author'

urlpatterns = [
    path('authors/', AuthorListView.as_view(), name='author-list'),
]
