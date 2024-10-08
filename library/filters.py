import django_filters
from .models import Library

class LibraryFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name="books__category__name", lookup_expr='icontains')
    author = django_filters.CharFilter(field_name="books__author__name", lookup_expr='icontains')

    class Meta:
        model = Library
        fields = ['category', 'author']
