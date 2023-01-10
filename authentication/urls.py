from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', RegisterAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path('set/<int:pk>/', SetUserInfoAPI.as_view()),
    path('google/login/', google_login, name='google_login'),
    path('google/callback/', google_callback, name='google_callback'),
    path('google/login/finish/', GoogleLogin.as_view(), name='google_login_todjango'),
    # path('rest-auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('kakao/login/', views.kakao_login, name='kakao_login'),
    path('kakao/callback/', views.kakao_callback, name='kakao_callback'),
    # path('kakao/logout/', auth_views.LogoutView.as_view()),
    path('logout/', LogoutAPI.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
