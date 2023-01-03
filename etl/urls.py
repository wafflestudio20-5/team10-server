from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *


urlpatterns = [
    path('classes/', ClassListView.as_view()),
    path('classes/create/', ClassCreateView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
