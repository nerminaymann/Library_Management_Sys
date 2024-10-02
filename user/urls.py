from django.urls import path
from django.contrib.auth import get_user_model
from .views import CreateUserView, CreateAuthTokenView, UpdateUserView

User = get_user_model()
app_name = 'user'

urlpatterns = [
    path('signup/',CreateUserView.as_view(),name='create'),
    path('token/',CreateAuthTokenView.as_view(),name='token'),
    path('me/', UpdateUserView.as_view(), name='me'),

]