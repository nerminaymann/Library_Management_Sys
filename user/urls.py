from django.urls import path
from django.contrib.auth import get_user_model
from .views import RegisterView, LoginView, UpdateUserView

User = get_user_model()
app_name = 'user'

urlpatterns = [
    path('signup/',RegisterView.as_view(),name='signup'),
    path('login/',LoginView.as_view(),name='login'),
    path('me/', UpdateUserView.as_view(), name='me'),

]