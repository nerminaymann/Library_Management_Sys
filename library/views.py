from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .filters import LibraryFilter
from .models import Library
from .serializers import LibrarySerializer

class LibraryListView(generics.ListAPIView):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = LibraryFilter