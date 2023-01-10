from rest_framework import generics, status
from authentication.serializers import *
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from django.contrib.auth.models import update_last_login
from django.shortcuts import redirect, reverse
from django.contrib import messages
from json import JSONDecodeError
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from .models import *
from .serializers import *
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.serializers import SocialLoginSerializer
from dj_rest_auth.registration.views import SocialLoginView
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from allauth.socialaccount.providers.google import views as google_view
from django.db import IntegrityError
import requests
import os

BASE_URL = 'http://localhost:8000/'


# exception
class SocialLoginException(Exception):
    pass


class KakaoException(Exception):
    pass


# 카카오 소셜 로그인
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

    messages.success(request, f"{user.email} signed up and logged in with Kakao")
    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    return redirect(f"{BASE_URL}authentication/set/{user.id}/")




# def kakao_logout(request):
#     admin_key = "d14d1a3bd680d2f9e9d383c76e361844"
#     logout_url = "https://kapi.kakao.com/v1/user/logout"
#     target_id = int(request.user.kakao_id)
#     data = {"target_id_type": "user_id", "target_id": target_id}
#     logout_res = requests.post(logout_url, headers={"Authorization": f"KakaoAK {admin_key}"}, data=data).json()
#     response = logout_res.get("id")
#
#     if target_id != response:
#         return Exception("Kakao Logout failed")
#     else:
#         print(str(response) + "Kakao Logout successed")
#
#     logout(request)
#
#     return redirect(f"{BASE_URL}authentication/login/")

# class KakaoView(View):
#     def get(self, request):
#         kakao_api = "https://kauth.kakao.com/oauth/authorize?response_type=code"
#         redirect_uri = "http://localhost:8000/authentication/kakao/callback/"
#         client_id = "52dd93ef1080aec2f79528f6aa8a9d68"
#
#         return redirect(f"{kakao_api}&client_id={client_id}&redirect_uri={redirect_uri}")
#
#
# class KakaoCallBackView(View):
#     def get(self, request):
#         data = {
#             "grant_type": "authorization_code",
#             "client_id": "52dd93ef1080aec2f79528f6aa8a9d68",
#             "redirection_uri": "http://localhost:8000/authentication/kakao/callback/",
#             "code": request.GET.get("code")
#         }
#
#         kakao_token_api = "https://kauth.kakao.com/oauth/token"
#         access_token = requests.post(kakao_token_api, data=data).json()["access_token"]
#         user_info = requests.get("https://kapi.kakao.com/v2/user/me", headers={"Authorization": f'Bearer ${access_token}'}).json()
#
#         return JsonResponse({"user_info": user_info})


# 구글 소셜로그인 변수 설정
SOCIAL_AUTH_GOOGLE_CLIENT_ID = "680552413143-pgfcofvs666rt227kjnb8pcvq0f2ov5j.apps.googleusercontent.com"
SOCIAL_AUTH_GOOGLE_SECRET = "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"
STATE = "google_login"

state = STATE
GOOGLE_CALLBACK_URI = BASE_URL + 'authentication/google/callback/'


# Create your views here.
def google_login(request):
    scope = "https://www.googleapis.com/auth/userinfo.email"
    client_id = SOCIAL_AUTH_GOOGLE_CLIENT_ID
    return redirect(
        f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}")


def google_callback(request):
    client_id = SOCIAL_AUTH_GOOGLE_CLIENT_ID
    client_secret = SOCIAL_AUTH_GOOGLE_SECRET
    code = request.GET.get('code')

    # 1. 받은 코드로 구글에 access token 요청
    token_req = requests.post(
        f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}&state={state}")

    ### 1-1. json으로 변환 & 에러 부분 파싱
    token_req_json = token_req.json()
    error = token_req_json.get("error")

    ### 1-2. 에러 발생 시 종료
    if error is not None:
        raise JSONDecodeError(error)

    ### 1-3. 성공 시 access_token 가져오기
    access_token = token_req_json.get('access_token')

    # 2. 가져온 access_token으로 이메일값을 구글에 요청
    email_req = requests.get(f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}")
    email_req_status = email_req.status_code

    ### 2-1. 에러 발생 시 400 에러 반환
    if email_req_status != 200:
        return JsonResponse({'err_msg': 'failed to get email'}, status=status.HTTP_400_BAD_REQUEST)

    ### 2-2. 성공 시 이메일 가져오기
    email_req_json = email_req.json()
    email = email_req_json.get('email')

    # return JsonResponse({'access': access_token, 'email':email})

    # 3. 전달 받은 이메일, access_token, code를 바탕으로 회원가입/로그인
    try:
        # 전달 받은 이메일로 등록된 유저가 있는지 탐색
        user = User.objects.get(email=email)
        print('username:', user.username)
        # FK로 연결되어 있는 socialaccount 테이블에서 해당 이메일의 유저가 있는지 확인
        social_user = SocialAccount.objects.get(user=user)
        print('email:', social_user.extra_data["email"])

        # 있는데 구글 계정이 아니면 에러
        if social_user.provider != 'google':
            return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)

        # 이미 Google로 제대로 가입된 유저 => 로그인 & 해당 유저의 jwt 발급
        data = {'access_token': access_token, 'code': code}
        # data = {'email': email, 'password': code}
        accept = requests.post(f"{BASE_URL}authentication/google/login/finish/", data=data)

        # print("checkhere: ", accept.text)

        # 뭔가 중간에 문제가 생기면 에러
        # accept_status = accept.status_code
        # if accept_status != 200:
        #     return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)

        accept_json = accept.json()
        print("accept_jsons", accept_json)
        accept_json.pop('user', None)
        return JsonResponse(accept_json)

    except User.DoesNotExist:
        # 전달받은 이메일로 기존에 가입된 유저가 아예 없으면 => 새로 회원가입 & 해당 유저의 jwt 발급
        data = {'access_token': access_token, 'code': code}
        # data = {'email': email, 'password': code, 'confirm_password': code}
        # print("data:", data)
        accept = requests.post(f"{BASE_URL}authentication/google/login/finish/", data=data)
        # SocialAccount.objects.create(user=user)
        # print("accept:", accept)
        accept_status = accept.status_code

        # 뭔가 중간에 문제가 생기면 에러
        # if accept_status != 200:
        #     return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)

        accept_json = accept.json()
        accept_json.pop('user', None)
        return JsonResponse(accept_json)

    except SocialAccount.DoesNotExist:
        # User는 있는데 SocialAccount가 없을 때 (=일반회원으로 가입된 이메일일때)
        return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = GOOGLE_CALLBACK_URI
    client_class = OAuth2Client
    serializer_class = SocialLoginSerializer

    # def get_serializer(self, *args, **kwargs):
    #     serializer_class = self.get_serializer_class()
    #     kwargs['context'] = self.get_serializer_context()
    #     return serializer_class(*args, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     serializer = RegisterSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #
    #     try:
    #         user, jwt_token = serializer.save()
    #         # UserSeminar.objects.create(user=user, is_instructor=False)
    #     except IntegrityError:
    #         return Response(status=status.HTTP_409_CONFLICT, data='이미 존재하는 유저 이메일입니다.')
    #
    #     return Response({'user': user.email, 'token': jwt_token}, status=status.HTTP_201_CREATED)


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


class LogoutAPI(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        user.auth_token.delete()
        # if Token.objects.get(user_id=user.id) is None:
        #     return Response(status=status.HTTP_404_NOT_FOUND)

        # Token.objects.delete(user=user)
        return Response(status=status.HTTP_200_OK)


class SetUserInfoAPI(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    # def update(self):
