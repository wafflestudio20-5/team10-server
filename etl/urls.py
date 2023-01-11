from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *


urlpatterns = [
    path('class/list/', ClassListCreateView.as_view()),
    path('class/professor-list/', ProfessorClassListCreateView.as_view()),
    path('class/delete/<int:pk>', ClassDeleteView.as_view()),
    path('class/enroll/', EnrollClassView.as_view()),
    path('class/drop/', DropClassView.as_view()),
    path('class/<int:pk>/user-list/', StudentListView.as_view()),
    # path('user-list/', UserListView.as_view()),
    path('assignments/', AssignmentListCreateView.as_view()),
    path('assignments/<int:pk>/', AssignmentClassView.as_view()),
    path('assignments/class/<int:pk>/', AssignmentListByLectureView.as_view()),
    path('assignments/student/', AssignmentListByStudentView.as_view()),
    path('assignments/grade/<int:pk>/', AssignmentGradeGetView.as_view()),
    path('assignments/grading/<int:pk>/', AssignmentGradingView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
