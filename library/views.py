import datetime
from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status
# from book.models import Transaction
# from .tasks import send_borrow_confirmation_email
from rest_framework.permissions import IsAuthenticated
from .filters import LibraryFilter
from .models import Library
from .serializers import LibrarySerializer
from rest_framework.response import Response

class LibraryListView(generics.ListAPIView):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = LibraryFilter
    permission_classes = [IsAuthenticated]

class LibraryDetailView(generics.RetrieveAPIView):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer
    permission_classes = [IsAuthenticated]
    def get_library(self,request,pk):
        book = get_object_or_404(Library, id=pk)
        serializer = LibrarySerializer(book)
        return Response(data = serializer.data,status=status.HTTP_200_OK)



