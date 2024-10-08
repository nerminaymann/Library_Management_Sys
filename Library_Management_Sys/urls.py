from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('user.urls', namespace='user')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('api/library/', include('library.urls', namespace='library')),
    path('api/author/', include('author.urls', namespace='author')),
    path('api/book/', include('book.urls', namespace='book')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger')

]