from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('user.urls', namespace='user')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('api/library/', include('library.urls', namespace='library')),
    path('api/author/', include('author.urls', namespace='author')),
    path('api/book/', include('book.urls', namespace='book')),

]
