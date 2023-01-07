from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *


urlpatterns = [
    path('classes/', ClassListView.as_view()),
    path('classes/create/', ClassCreateView.as_view()),
    path('<int:pk>/enroll/', EnrollClassView.as_view()),
    path('<int:pk>/drop/', DropClassView.as_view()),
    path('class/<int:pk>/user-list/', StudentListView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
