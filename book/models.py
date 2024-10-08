from datetime import timedelta

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils import timezone
from django.db import models
from Library_Management_Sys import settings
from library.models import Library
from author.models import Author
from user.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author,related_name='books', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='books',on_delete=models.SET_NULL, null=True)
    library = models.ForeignKey(Library,related_name='books', on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    copies = models.IntegerField(default=1)

    def __str__(self):
        return self.title

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(default=timezone.now)
    return_date = models.DateTimeField(null=True, blank=True)  # the expected maximum return date
    actual_return_date = models.DateTimeField(null=True, blank=True)  # filled when the book is returned
    returned = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.borrow_date and not self.return_date:
            self.return_date = self.borrow_date + timedelta(days=30)

        # When a transaction is created (borrowing), mark the book as unavailable
        if not self.returned:
            self.book.is_available = False
        else:
            self.actual_return_date = timezone.now()
            self.book.is_available = True
        self.book.save()
        super().save(*args, **kwargs)

    def return_book(self):
        # When a book is returned
        #if self.returned:
        self.actual_return_date = timezone.now()
        self.book.is_available = True
        self.book.save()
        self.save()


    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title} from {self.library.name} at {self.borrow_date}"

# class Transaction(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     book = models.ForeignKey(Book, on_delete=models.CASCADE)
#     borrow_date = models.DateTimeField(auto_now_add=True)
#     return_date = models.DateTimeField(null=True, blank=True)
#
#     def save(self, *args, **kwargs):
#         # Notify real-time WebSocket clients
#         channel_layer = get_channel_layer()
#         if self.return_date:
#             self.book.is_available = True
#             message = f"'{self.book.title}' is now available."
#         else:
#             self.book.is_available = False
#             message = f"'{self.book.title}' has been borrowed."
#
#         self.book.save()
#
#         # Send message to WebSocket group
#         async_to_sync(channel_layer.group_send)(
#             "book_availability", {
#                 "type": "book_availability_update",
#                 "message": message
#             }
#         )
#         super().save(*args, **kwargs)