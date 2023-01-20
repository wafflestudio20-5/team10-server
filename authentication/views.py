from rest_framework import generics, status
from authentication.serializers import *
from rest_framework.response import Response
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.tokens import RefreshToken
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
from rest_framework.views import APIView
from django.db import IntegrityError
from json import JSONDecodeError
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.models import SocialAccount
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from team10_server.settings import SECRET_KEY, ALGORITHM
from django.http import HttpResponse

# Create your views here.

# jwt 토큰 사용을 위한 기본 세팅
JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


def jwt_token_of(user):
    payload = JWT_PAYLOAD_HANDLER(user)
    jwt_token = JWT_ENCODE_HANDLER(payload)
    return jwt_token


class RegisterAPI(generics.CreateAPIView):
    serializer_class = RegisterSerializer


class LoginAPI(generics.CreateAPIView):
    serializer_class = UserLoginSerializer

    @swagger_auto_schema(
        request_body=swaggers.login_request_body,
        responses=swaggers.login_responses,
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data

        return Response({'success': True, 'token': token}, status=status.HTTP_200_OK)


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
        response = JsonResponse({
            "message": "success"
        })
        response.delete_cookie('jwt')
        return response


# @csrf_exempt
# def logout(request):
#     if request.method == 'POST':
#         response = JsonResponse({
#             "message": "success"
#         })
#         response.delete_cookie('jwt')
#         return response


BASE_URL = 'http://localhost:8000/'
KAKAO_CALLBACK_URI = BASE_URL + 'authentication/kakao/callback/'


class KakaoLoginView(APIView):
    def get(self, request):
        kakao_api = "https://kauth.kakao.com/oauth/authorize?response_type=code"
        redirect_uri = KAKAO_CALLBACK_URI
        client_id = "52dd93ef1080aec2f79528f6aa8a9d68"

        return redirect(f"{kakao_api}&client_id={client_id}&redirect_uri={redirect_uri}")


class KakaoCallBackView(APIView):
    def get(self, request):

        code = request.GET.get("code", None)
        data = {
            "grant_type": "authorization_code",
            "client_id": "52dd93ef1080aec2f79528f6aa8a9d68",
            "redirection_uri": "http://localhost:8000/authentication/kakao/callback/",
            "code": code
        }

        kakao_token_api = "https://kauth.kakao.com/oauth/token"
        access_token_json = requests.post(kakao_token_api, data=data).json()

        access_token = access_token_json["access_token"]
        user_info = requests.get("https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {access_token}"})
        user_json = user_info.json()

        # kakao_id = user_json.get("id")
        kakao_account = user_json.get("kakao_account")
        email = kakao_account.get("email", None)

        data = {
            "access_token": access_token,
            "code": code
        }

        print('email:', email)

        try:
            user = User.objects.get(email=email)
            update_last_login(None, user)
            token = RefreshToken.for_user(user=user)

            data = {
                'user': user.id,
                'refresh_token': str(token),
                'access_token': str(token.access_token)
            }

            return JsonResponse(data)

            # jwt_token = jwt.encode({'id': user.id}, SECRET_KEY, ALGORITHM)

            # social_user = SocialAccount.objects.get(user=user)
            # accept = requests.post(
            #     f"{BASE_URL}/authentication/kakao/login/finish/", data=data
            # )
            # accept_json = accept.json()
            # accept_json.pop("user", None)
            # output = redirect("https://www.naver.com/")
            # return HttpResponse(f'id:{user.id}, name:{user.name}, token:{jwt_token}, exist:true')

        except User.DoesNotExist:
            # accept = requests.post(
            #     f"{BASE_URL}/authentication/kakao/login/finish/", data=data
            # )
            # accept_json = accept.json()
            # accept_json.pop("user", None)
            user = User.objects.create_user(email=email)
            user.is_social_login = True
            user.save()
            SocialAccount.objects.create(user=user)

            update_last_login(None, user)
            token = RefreshToken.for_user(user=user)

            data = {
                'user': user.id,
                'refresh_token': str(token),
                'access_token': str(token.access_token)
            }

            # return redirect(f"{BASE_URL}authentication/set/{user.id}/")
            return JsonResponse(data)

            # jwt_token = jwt.encode({'id': user.id}, SECRET_KEY, ALGORITHM)
            # return HttpResponse(f'id:{user.id}, name:{user.name}, token:{jwt_token}, exist:false')


class KakaoLogin(SocialLoginView):
    adapter_class = kakao_view.KakaoOAuth2Adapter
    callback_url = KAKAO_CALLBACK_URI
    client_class = OAuth2Client

