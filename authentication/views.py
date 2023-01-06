from rest_framework import generics, status
from authentication.serializers import *
from django.contrib.auth import authenticate
from rest_framework.response import Response
from django.contrib.auth.models import update_last_login
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny


# Create your views here.
class RegisterAPI(generics.CreateAPIView):
    serializer_class = RegisterSerializer


class LoginAPI(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        user = authenticate(email=email, password=password)
        if user is None:
            return Response({"email": "not correct"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            update_last_login(None, user)
            token, _ = Token.objects.get_or_create(user=user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )
        serializer = UserSerializer(user)
        return Response(serializer.data)


class SetUserInfoAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all().filter(email=self.request.user) #현재 접속중인 user의 정보만 반환(보안)


class IdCheckAPI(generics.CreateAPIView):
    serializer_class = UserIDSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"email": "valid"}, status=status.HTTP_200_OK)


class LogoutAPI(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)