from django.urls import path
from .views import LibraryListView, LibraryDetailView

app_name = 'library'
urlpatterns = [
    path('libraries/', LibraryListView.as_view(), name='library-list'),
    path('libraries/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),
]
