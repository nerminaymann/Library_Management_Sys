from django.contrib.auth import get_user_model, authenticate
from rest_framework import generics, authentication, permissions, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, LoginSerializer,OtherUsersSerializer

User = get_user_model()

#-----------------------------------REGISTRATION-----------------------------------------
class RegisterView(generics.GenericAPIView):
    # queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        permissions.AllowAny]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -----------------------------------LOGIN AND GENERATE TOKEN-------------------------------------
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [
        permissions.AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            # user = serializer.validated_data
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            user = authenticate(username=email, password=password)
            if user is None:
                return Response({"data": {}, "message": "user is not found"}, status=status.HTTP_400_BAD_REQUEST)
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -----------------------------------UPDATE USER PROFILE-------------------------------------
class UpdateUserView(generics.RetrieveUpdateAPIView):
    #Manage the Authenticated User
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

# -----------------------------------UPDATE USER INFO-------------------------------------

class UpdateOtherUsersView(generics.RetrieveUpdateAPIView):
    #Manage the Authenticated User
    queryset = User.objects.all()
    serializer_class = OtherUsersSerializer
    permission_classes = [permissions.IsAdminUser]

