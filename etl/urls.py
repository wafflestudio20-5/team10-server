from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *


urlpatterns = [
    path('class/', ClassListCreateView.as_view()),
    path('class/professor/', ProfessorClassListCreateView.as_view()),
    path('class/<int:pk>/', ClassDeleteView.as_view()),
    path('class/enroll/', EnrollClassView.as_view()),
    path('class/drop/', DropClassView.as_view()),
    path('class/<int:pk>/user-list/', StudentListView.as_view()),
    path('user-list/', UserListView.as_view()),

    # 과제
    path('assignments/', AssignmentListCreateView.as_view()),
    path('assignments/<int:pk>/', AssignmentClassView.as_view()),
    path('assignments/class/<int:pk>/', AssignmentListByLectureView.as_view()),
    path('assignments/student/', AssignmentListByStudentView.as_view()),
    path('assignments/<int:pk>/score/', AssignmentGradeGetView.as_view()),
    path('assignments/<int:pk>/grading/', AssignmentGradingView.as_view()),
    path('assignments/<int:pk>/upload/', AssignmentUploadView.as_view()),
    path('assignments/<int:pk>/download/', AssignmentDownloadView.as_view()),
    path('assignments/<int:pk>/user/<int:user_pk>/download/', AssignmentDownloadView.as_view()),

    # 공지사항 게시판
    path('class/<int:pk>/announcements/', AnnouncementListCreateView.as_view()),
    path('announcement/<int:pk>/', AnnouncementDetailView.as_view()),

    # 질의응답 게시판
    path('class/<int:pk>/questions/', QuestionListCreateView.as_view()),
    path('question/<int:pk>/', QuestionDetailView.as_view()),

    # 댓글
    path('post/<int:pk>/comments/', CommentCreateView.as_view()),
    path('comment/<int:pk>/', CommentDetailView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
