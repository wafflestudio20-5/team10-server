from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *


urlpatterns = [
    path('signup/', RegisterAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path('logout/', LogoutAPI.as_view()),
    path('idcheck/', IdCheckAPI.as_view()),
    path('student/<int:pk>/', DeleteStudentView.as_view()),
    path('kakao/login/', KakaoLoginView.as_view()),
    path('kakao/callback/', KakaoCallBackView.as_view()),
    path('profile/', ProfileUploadView.as_view()),
    path('change-password/', ChangePasswordView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
