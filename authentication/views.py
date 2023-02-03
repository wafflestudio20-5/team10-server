import os
import boto3
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


# TODO: 로그인 여러 번 시도해서 액세스 토큰을 새로 발급 받아도, 이전 액세스 토큰은 비활성화되지 않는 것이 정상이 맞나?(잘 모름)
class LoginAPI(generics.CreateAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [IsAdmin | ~IsAuthenticated]

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
    permission_classes = [IsAdmin | ~IsAuthenticated]

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

    # TODO: Insomnia로 확인해보니 logout 후에도 토큰이 잘 작동. 정상 작동하는 것인지 확인 필요.
    @swagger_auto_schema(
        operation_description=swaggers.logout_operation_description,
        responses=swaggers.logout_responses,
    )
    def get(self, request, *args, **kwargs):
        response = JsonResponse({
            "success": True
        })
        response.delete_cookie('jwt')
        return response


BASE_URL = 'http://etlclone-env.eba-dxtv92ct.ap-northeast-2.elasticbeanstalk.com/'
# BASE_URL = 'http://127.0.0.1:8000/'
KAKAO_CALLBACK_URI = BASE_URL + 'authentication/kakao/callback/'
LOGOUT_URL = BASE_URL + 'authentication/logout/'
LOGIN_URL = BASE_URL + 'authentication/login/'


class KakaoLoginView(APIView):
    def get(self, request):
        kakao_api = os.environ.get('KAKAO_API')
        redirect_uri = KAKAO_CALLBACK_URI
        client_id = os.environ.get('KAKAO_CLIENT_ID')

        return redirect(f"{kakao_api}&client_id={client_id}&redirect_uri={redirect_uri}")


class KakaoCallBackView(APIView):
    def post(self, request):
        code = request.data.get("code", None)

        data = {
            "grant_type": "authorization_code",
            "client_id": os.environ.get('KAKAO_CLIENT_ID'),
            "redirection_uri": f"{BASE_URL}authentication/kakao/callback/",
            "code": code
        }

        kakao_token_api = "https://kauth.kakao.com/oauth/token"
        access_token_json = requests.post(kakao_token_api, data=data).json()

        access_token = access_token_json["access_token"]
        user_info = requests.get("https://kapi.kakao.com/v2/user/me",
                                 headers={"Authorization": f"Bearer {access_token}"})
        user_json = user_info.json()

        kakao_id = str(user_json.get("id", "1111111111"))
        kakao_account = user_json.get("kakao_account")
        email = kakao_account.get("email", "team10@waffle.com")

        try:
            user = User.objects.get(email=email)
            update_last_login(None, user)
            token = RefreshToken.for_user(user=user)

            data = {
                'user': user.id,
                'refresh_token': str(token),
                'access_token': str(token.access_token)
            }

            return Response(data=data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            user = User.objects.create_user(email=email)
            user.is_social_login = True
            user.kakao_id = kakao_id
            user.save()
            # SocialAccount.objects.create(user=user)

            update_last_login(None, user)
            token = RefreshToken.for_user(user=user)

            data = {
                'user': user.id,
                'refresh_token': str(token),
                'access_token': str(token.access_token)
            }

            # return redirect(f"{BASE_URL}authentication/set/{user.id}/")
            return Response(data=data, status=status.HTTP_201_CREATED)


class KakaoLogoutView(APIView):
    def get(self, request):
        kakao_rest_api_key = os.environ.get('KAKAO_CLIENT_ID')
        logout_redirect_uri = LOGOUT_URL
        state = "none"
        kakao_service_logout_url = "https://kauth.kakao.com/oauth/logout"
        res = requests.get(f"{kakao_service_logout_url}?client_id={kakao_rest_api_key}&logout_redirect_uri={logout_redirect_uri}&state={state}")
        return Response(data="Kakao Logout Success", status=res.status_code)


class KakaoDisconnect(APIView):
    def post(self, request):
        user = request.user
        kakao_admin_key = os.environ.get('KAKAO_ADMIN_KEY')
        kakao_service_disconnect_url = "https://kapi.kakao.com/v1/user/unlink"
        headers = {"Authorization": f"KakaoAK {kakao_admin_key}"}
        data = {"target_id_type": "user_id", "target_id": int(user.kakao_id)}
        res = requests.post(kakao_service_disconnect_url, headers=headers, data=data)

        deleted_user_id = str(res.json().get("id"))
        print("deleted_user_id: ", deleted_user_id)
        if deleted_user_id == user.kakao_id:
            data_ = "Success Kakao Disconnect"
        else:
            data_ = "Fail Kakao Disconnect"

        return Response(data=data_, status=status.HTTP_200_OK)


class ProfileUploadView(views.APIView):
    parser_classes = [MultiPartParser, ]
    permission_classes = (IsAdminOrQualified,)

    @swagger_auto_schema(
        operation_description=swaggers.profile_put_operation_description,
        request_body=AssignmentFileSerializer
    )
    def put(self, request, format=None):
        if 'file' not in request.data:
            Response(status=status.HTTP_400_BAD_REQUEST)
        profile_obj = request.data.get('file', None)
        self.request.user.profile.save(profile_obj.name, profile_obj, save=True)
        return Response(status=status.HTTP_201_CREATED)


class ProfileDownloadView(views.APIView):
    permission_classes = (IsAdminOrQualified,)
    def get(self, request, format=None):
        path = self.request.user.profile.name
        s3 = boto3.client('s3',region_name=os.environ.get('AWS_REGION'), aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))
        url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': 'etl-media-database',
                'Key': path,
            },
            ExpiresIn=600
        )
        data = {
            'download_link': url
        }
        return JsonResponse(data, status=status.HTTP_200_OK)


class ChangePasswordView(generics.CreateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description=swaggers.change_password_operation_description,
        request_body=swaggers.change_password_request,
        responses=swaggers.change_password_responses,
    )
    def post(self, request, *args, **kwargs):
        password = request.data['password']
        new_password = request.data['new_password']

        if not check_password(password, request.user.password):
            return Response({"error": "wrong password."}, status=status.HTTP_400_BAD_REQUEST)

        if len(new_password) < 8:
            return Response({"error": "too short password. password length should be >=8."},
                            status=status.HTTP_400_BAD_REQUEST)
        same_with_before_password = password == new_password
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
    permission_classes = [IsAdmin | (IsAuthenticated & DoesUserMatchRequest)]

    @swagger_auto_schema(
        operation_description=swaggers.user_get_operation_description,
        responses=swaggers.user_get_responses,
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description=swaggers.user_patch_operation_description,
        request_body=swaggers.user_patch_request_body,
        responses=swaggers.user_patch_responses
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, *kwargs)

    @swagger_auto_schema(
        operation_description=swaggers.user_delete_operation_description,
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
