import django_filters
from .models import Author

class AuthorFilter(django_filters.FilterSet):
    library = django_filters.CharFilter(field_name="books__library__name", lookup_expr="icontains")
    category = django_filters.CharFilter(field_name="books__category__name", lookup_expr="icontains")

    class Meta:
        model = Author
        fields = ['library', 'category']
