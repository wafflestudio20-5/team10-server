from rest_framework import generics, status
from authentication.serializers import *
from django.contrib.auth import authenticate
from rest_framework.response import Response
from django.contrib.auth.models import update_last_login


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
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )

        serializer = UserSerializer(user)
        return Response(serializer.data)


class SetUserInfoAPI(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

