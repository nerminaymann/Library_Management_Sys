from django.contrib import admin

from book.models import Book, Category,Transaction

admin.site.register(Category)

class TransactionAdmin(admin.ModelAdmin):
    ordering = ['-borrow_date']
    list_display = ['user','book','library','borrow_date','returned']

admin.site.register(Transaction, TransactionAdmin)

class BookAdmin(admin.ModelAdmin):
    ordering = ['title']
    list_display = ['title','author','category','library']
    # list_filter =

admin.site.register(Book, BookAdmin)