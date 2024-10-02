from django.contrib.auth import get_user_model
from rest_framework import generics,authentication,permissions

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from .serializers import UserSerializer, AuthTokenSerializer

User = get_user_model()

#-----------------------------------REGISTRATION-----------------------------------------
class CreateUserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# -----------------------------------LOGIN AND GENERATE TOKEN-------------------------------------
class CreateAuthTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


# -----------------------------------UPDATE USER PROFILE-------------------------------------
class UpdateUserView(generics.RetrieveUpdateAPIView):
    #Manage the Authenticated User
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_class = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


