from django.contrib import admin

from book.models import Book, Category

admin.site.register(Book)
# admin.site.register(BorrowTransaction)
# admin.site.register(ReturnTransaction)
admin.site.register(Category)
