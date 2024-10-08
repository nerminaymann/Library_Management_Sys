from django.contrib import admin

from book.models import Book, Category,Transaction

admin.site.register(Book)
admin.site.register(Transaction)
# admin.site.register(ReturnTransaction)
admin.site.register(Category)
