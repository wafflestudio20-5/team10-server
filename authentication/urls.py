from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *


urlpatterns = [
    path('signup/', RegisterAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path('logout/', LogoutAPI.as_view()),
    path('idcheck/', IdCheckAPI.as_view()),
    path('student/<int:pk>/drop-out/', DropOutView.as_view()),
    path('kakao/login/', kakao_login, name='kakao_login'),
    path('kakao/callback/', kakao_callback, name='kakao_callback'),
    path('change-password/', ChangePasswordView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
