from django.contrib import admin

from book.models import Book, BorrowTransaction, ReturnTransaction, Category

# Register your models here.

admin.site.register(Book)
admin.site.register(BorrowTransaction)
admin.site.register(ReturnTransaction)
admin.site.register(Category)
