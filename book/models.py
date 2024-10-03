from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils import timezone
from django.db import models
from Library_Management_Sys import settings
from library.models import Library
from author.models import Author
from user.models import User


# from django.contrib.auth.models import User

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

# class BorrowTransaction(models.Model):
#             book = models.ForeignKey(Book, on_delete=models.CASCADE)
#             borrower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#             borrowed_at = models.DateTimeField(auto_now_add=True)
#             due_date = models.DateField()
#             returned_at = models.DateTimeField(null=True, blank=True)
#
#             def is_overdue(self):
#                 if self.returned_at is None and self.due_date < timezone.now().date():
#                     return True
#                 return False
#
#             def __str__(self):
#                 return f"{self.book} - {self.borrower} - {self.due_date}"
#
#
# class ReturnTransaction(models.Model):
#     borrow_transaction = models.OneToOneField(BorrowTransaction, on_delete=models.CASCADE)
#     return_date = models.DateTimeField(default=timezone.now)
#
#     def __str__(self):
#         return f"{self.borrow_transaction.borrower} - {self.return_date}"


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Notify real-time WebSocket clients
        channel_layer = get_channel_layer()
        if self.return_date:
            self.book.is_available = True
            message = f"'{self.book.title}' is now available."
        else:
            self.book.is_available = False
            message = f"'{self.book.title}' has been borrowed."

        self.book.save()

        # Send message to WebSocket group
        async_to_sync(channel_layer.group_send)(
            "book_availability", {
                "type": "book_availability_update",
                "message": message
            }
        )
        super().save(*args, **kwargs)