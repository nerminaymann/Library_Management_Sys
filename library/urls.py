from django.urls import path
from .views import LibraryListView

app_name = 'library'
urlpatterns = [
    path('libraries/', LibraryListView.as_view(), name='library-list'),
]
