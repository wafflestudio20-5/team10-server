from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *
from . import views

urlpatterns = [
    path('signup/', RegisterAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path('logout/', LogoutAPI.as_view()),
    path('set/<int:pk>/', SetUserInfoAPI.as_view()),
    path('idcheck/', IdCheckAPI.as_view()),
    path('kakao/login/', KakaoLoginView.as_view()),
    path('kakao/callback/', KakaoCallBackView.as_view()),
    path('kakao/login/finish/', KakaoLogin.as_view()),
]

