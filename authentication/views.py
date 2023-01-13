from rest_framework import generics, status
from authentication.serializers import *
from rest_framework.response import Response
from django.contrib.auth.models import update_last_login
from rest_framework.permissions import IsAuthenticated
from .permissions import *
import authentication.swaggers as swaggers
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authtoken.models import Token
import requests
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages


# Create your views here.
class RegisterAPI(generics.CreateAPIView):
    serializer_class = RegisterSerializer


class LoginAPI(generics.CreateAPIView):
    serializer_class = UserLoginSerializer

    @swagger_auto_schema(
        request_body=swaggers.login_request_body,
        responses=swaggers.login_responses,
    )
    def post(self, request, *args, **kwargs):
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        user = authenticate(email=email, password=password)
        if user is None:
            return Response({"error": "email or password is not correct"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            update_last_login(None, user)
            token, _ = Token.objects.get_or_create(user=user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )
        serializer = UserLoginSerializer(user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# 현진님의 코드 조금 수정함. 유저가 자신의 정보에만 접근할 수 있도록 permissions.py를 추가했음.
class SetUserInfoAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [DoesUserMatchRequest]
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()


class IdCheckAPI(generics.CreateAPIView):
    serializer_class = UserIDSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"email": "valid"}, status=status.HTTP_200_OK)


class LogoutAPI(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserDetailSerializer

    def get(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


BASE_URL = 'http://localhost:8000/'


# exception
class SocialLoginException(Exception):
    pass


class KakaoException(Exception):
    pass


def kakao_login(request):
    # if request.user.is_authenticated:
    #     raise SocialLoginException("User already logged in, 1")
    kakao_api = "https://kauth.kakao.com/oauth/authorize?response_type=code"
    redirect_uri = "http://localhost:8000/authentication/kakao/callback/"
    client_id = "52dd93ef1080aec2f79528f6aa8a9d68"

    return redirect(f"{kakao_api}&client_id={client_id}&redirect_uri={redirect_uri}")


def kakao_callback(request):
    # if request.user.is_authenticated:
    #     raise SocialLoginException("User already logged in, 2")

    code = request.GET.get("code", None)
    if code is None:
        KakaoException("Can't get code")

    data = {
        "grant_type": "authorization_code",
        "client_id": "52dd93ef1080aec2f79528f6aa8a9d68",
        "redirection_uri": "http://localhost:8000/authentication/kakao/callback/",
        "code": code
    }

    kakao_token_api = "https://kauth.kakao.com/oauth/token"
    access_token_json = requests.post(kakao_token_api, data=data).json()

    error = access_token_json.get("error", None)

    if error is not None:
        print(error)
        KakaoException("Can't get access token")

    access_token = access_token_json["access_token"]
    user_info = requests.get("https://kapi.kakao.com/v2/user/me", headers={"Authorization": f'Bearer ${access_token}'}).json()

    kakao_id = user_info.get("id")
    kakao_account = user_info.get("kakao_account")
    email = kakao_account.get("email", None)

    try:
        user = User.objects.get(email=email)
    except ObjectDoesNotExist:
        user = None

    if user is None:
        user = User.objects.create_user(email=email)
        Token.objects.create(user=user)
        user.set_unusable_password()
        user.save()
        return redirect(f"{BASE_URL}authentication/set/{user.id}/")

    messages.success(request, f"{user.email} signed up and logged in with Kakao")
    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    # return redirect(f"{BASE_URL}etl/announcement/")
    return redirect("https://www.naver.com")
