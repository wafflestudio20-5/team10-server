import os
from rest_framework import generics, status, views
from authentication.serializers import *
from rest_framework.response import Response
from django.contrib.auth.models import update_last_login
from rest_framework.permissions import IsAuthenticated
from .permissions import *
import authentication.swaggers as swaggers
from drf_yasg.utils import swagger_auto_schema
import requests
from django.shortcuts import redirect
from rest_framework.parsers import MultiPartParser
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from allauth.socialaccount.models import SocialAccount
from etl.serializers import AssignmentFileSerializer


# Create your views here.
class RegisterAPI(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [IsAdmin | ~IsAuthenticated]

    @swagger_auto_schema(
        operation_description=swaggers.register_operation_description,
        responses=swaggers.register_responses
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class LoginAPI(generics.CreateAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [IsAdmin | ~IsAuthenticated]

    # TODO: swagger 수정 필요
    @swagger_auto_schema(
        operation_description=swaggers.login_operation_description,
        request_body=swaggers.login_request_body,
        responses=swaggers.login_responses,
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data
        return Response({'success': True, 'token': token}, status=status.HTTP_200_OK)


class IdCheckAPI(generics.CreateAPIView):
    serializer_class = UserIDSerializer
    permission_classes = [~IsAuthenticated]

    @swagger_auto_schema(
        operation_description=swaggers.idcheck_operation_description,
        responses=swaggers.idcheck_operation_responses,
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"email": "valid"}, status=status.HTTP_200_OK)


class LogoutAPI(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserDetailSerializer

    @swagger_auto_schema(
        operation_description=swaggers.logout_operation_description,
        responses=swaggers.logout_responses,
    )
    def get(self, request, *args, **kwargs):
        response = JsonResponse({
            "message": "success"
        })
        response.delete_cookie('jwt')
        return response


# BASE_URL = 'https://test-project10.onrender.com'
BASE_URL = 'http://localhost:8000/'
KAKAO_CALLBACK_URI = BASE_URL + 'authentication/kakao/callback/'


class KakaoLoginView(APIView):
    def get(self, request):
        kakao_api = os.environ.get('KAKAO_API')
        redirect_uri = KAKAO_CALLBACK_URI
        client_id = os.environ.get('KAKAO_CLIENT_ID')

        return redirect(f"{kakao_api}&client_id={client_id}&redirect_uri={redirect_uri}")


class KakaoCallBackView(APIView):
    def get(self, request):
        code = request.GET.get("code", None)
        data = {
            "grant_type": "authorization_code",
            "client_id": os.environ.get('KAKAO_CLIENT_ID'),
            "redirection_uri": "http://localhost:8000/authentication/kakao/callback/",
            "code": code
        }

        kakao_token_api = "https://kauth.kakao.com/oauth/token"
        access_token_json = requests.post(kakao_token_api, data=data).json()

        access_token = access_token_json["access_token"]
        user_info = requests.get("https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {access_token}"})
        user_json = user_info.json()

        kakao_account = user_json.get("kakao_account")
        email = kakao_account.get("email", None)

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

        except User.DoesNotExist:
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


class ProfileUploadView(views.APIView):
    parser_classes = [MultiPartParser, ]
    permission_classes = [IsQualified]

    @swagger_auto_schema(
        operation_description=swaggers.profile_put_operation_description,
        request_body=AssignmentFileSerializer
    )
    def put(self, request, format=None):
        if 'file' not in request.data:
            Response(status=status.HTTP_400_BAD_REQUEST)
        profile_obj = request.data.get('file',None)
        self.request.user.profile.save(profile_obj.name, profile_obj, save=True)
        return Response(status=status.HTTP_201_CREATED)


class ChangePasswordView(generics.CreateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description=swaggers.change_password_operation_description,
        request_body=swaggers.change_password_request,
        responses=swaggers.change_password_responses,
    )
    def post(self, request, *args, **kwargs):
        new_password = request.data['new_password']
        if len(new_password) < 8:
            return Response({"error": "too short password. password length should be >=8."}, status=status.HTTP_400_BAD_REQUEST)
        same_with_before_password = check_password(new_password, request.user.password)
        if same_with_before_password:
            return Response({"error": "same with previous password."}, status=status.HTTP_400_BAD_REQUEST)
        request.user.set_password(new_password)
        request.user.save()
        return Response({"success": "new password has been set."}, status=status.HTTP_201_CREATED)


# 디버깅용 모든 유저의 정보를 보는 View
class UserListView(generics.ListAPIView):
    permission_classes = [IsAdmin]
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer

    @swagger_auto_schema(
        operation_description=swaggers.users_operation_description,
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsAdmin | (IsAuthenticated & DoesUserMatchRequestOrReadOnly)]

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, *kwargs)

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
