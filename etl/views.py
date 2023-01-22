from .serializers import *
from rest_framework import generics, status, views
from rest_framework.permissions import IsAuthenticated
from .models import *
from .permissions import *
from .paginations import *
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
import etl.swaggers as swaggers
from rest_framework.parsers import MultiPartParser


# TODO: 페이지네이션 추가해야 함
class ClassListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdmin | (IsAuthenticated & IsProfessorOrReadOnly)]
    queryset = Class.objects.all()
    serializer_class = ClassSerializer

    @swagger_auto_schema(
        operation_description=swaggers.classes_get_operation_description
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description=swaggers.classes_post_operation_description,
        request_body=swaggers.classes_post_request_body,
        responses=swaggers.classes_post_responses,
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ProfessorClassListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdmin | (IsAuthenticated & IsQualified & IsProfessor)]
    serializer_class = ClassSerializer

    def get_queryset(self):
        return Class.objects.filter(created_by=self.request.user)

    @swagger_auto_schema(
        operation_description=swaggers.class_professor_get_operation_description,
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description=swaggers.class_professor_post_operation_description,
        request_body=swaggers.classes_post_request_body,
        responses=swaggers.class_professor_post_responses,
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ClassDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAdmin | IsCreatorReadOnly]
    queryset = Class.objects.all()

    @swagger_auto_schema(
        operation_description=swaggers.class_delete_operation_description,
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class EnrollClassView(generics.CreateAPIView):
    permission_classes = [IsAdmin | (IsAuthenticated & IsQualified & (~IsProfessor))]
    serializer_class = EnrollDropSerializer

    @swagger_auto_schema(
        operation_description=swaggers.class_enroll_operation_description,
        request_body=swaggers.class_enroll_request_body,
        responses=swaggers.class_enroll_responses,
    )
    def post(self, request, *args, **kwargs):
        class_id = int(request.data['class_id'])
        lecture = Class.objects.get(id=class_id)
        for l in lecture.assignment_set.all():
            l.student.add(request.user)
        request.user.classes.add(lecture)
        serializer = EnrollDropSerializer(request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class DropClassView(generics.CreateAPIView):
    permission_classes = [IsAdmin | (IsAuthenticated & IsQualified & (~IsProfessor))]
    serializer_class = EnrollDropSerializer

    @swagger_auto_schema(
        operation_description=swaggers.class_drop_operation_description,
        request_body=swaggers.class_drop_request_body,
        responses=swaggers.class_drop_responses,
    )
    def post(self, request, *args, **kwargs):
        class_id = int(request.data['class_id'])
        lecture = Class.objects.get(id=class_id)
        for l in lecture.assignment_set.all():
            l.student.remove(request.user)
        request.user.classes.remove(lecture)
        serializer = EnrollDropSerializer(request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class StudentListView(generics.ListAPIView):
    pagination_class = StudentListPagination
    serializer_class = UserSimpleSerializer
    permission_classes = [IsAdmin | (IsAuthenticated & IsQualified)]

    def get_queryset(self):
        return User.objects.filter(classes=self.kwargs['pk'])

    @swagger_auto_schema(
        operation_description=swaggers.class_user_list_operation_description,
        responses=swaggers.class_user_list_responses,
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


# 모든 assignments list 반환
class AssignmentListCreateView(generics.ListCreateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentCreateSerializer
    permission_classes = [IsProfessorOrReadOnly | IsAdmin]

    @swagger_auto_schema(
        operation_description=swaggers.assignments_post_operation_description,
        request_body=swaggers.assignments_post_request_body,
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description=swaggers.assignments_get_operation_description,
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


# pk번째 assignments detail 반환, 수정, 삭제
class AssignmentClassView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentDetailSerializer
    permission_list = {
        'PATCH': [IsCreatorReadOnly | IsAdmin],
        'PUT': [IsCreatorReadOnly | IsAdmin],
        'DELETE': [IsCreatorReadOnly | IsAdmin],
        'GET': [IsQualified]
    }

    def get_permissions(self):
        if self.request.method in self.permission_list:
            permission_classes = self.permission_list.get(self.request.method)
            return [permission() for permission in permission_classes]
        return super().get_permissions()

    @swagger_auto_schema(
        operation_description=swaggers.assignments_class_get_operation_description
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description=swaggers.assignments_class_put_operation_description
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description=swaggers.assignments_class_patch_operation_description
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description=swaggers.assignments_class_delete_operation_description
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


# pk번째 class의 모든 assignment list 반환
class AssignmentListByLectureView(generics.ListAPIView):
    serializer_class = AssignmentCreateSerializer
    permission_classes = [IsQualified]

    def get_queryset(self):
        return Assignment.objects.all().filter(lecture=self.kwargs['pk'])

    @swagger_auto_schema(
        operation_description=swaggers.assignments_list_lecture_get_operation_description,
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


# 학생이 자신의 모든 assignment list 반환
class AssignmentListByStudentView(generics.ListAPIView):
    serializer_class = AssignmentCreateSerializer
    permission_classes = [IsQualified]

    def get_queryset(self):
        return Assignment.objects.all().filter(student=self.request.user)

    @swagger_auto_schema(
        operation_description=swaggers.assignments_list_student_get_operation_description,
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


# 학생이 pk번째 assignment 점수, 제출여부, 채점여부 확인
class AssignmentGradeGetView(generics.RetrieveAPIView):
    serializer_class = AssignmentToStudentSerializer
    permission_classes = [IsQualified]

    @swagger_auto_schema(
        operation_description=swaggers.assignments_grade_get_operation_description,
    )
    def get(self, request, *args, **kwargs):
        obj = AssignmentToStudent.objects.get(assignment=self.kwargs['pk'], student=self.request.user)
        serializer = AssignmentToStudentSerializer(obj)
        return Response(serializer.data)


# 교수자가 pk번째 assignments 채점. 학번, 점수 입력
class AssignmentGradingView(generics.UpdateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentGradingSerializer
    permission_classes = [IsCreatorReadOnly | IsAdmin]

    @swagger_auto_schema(
        operation_description=swaggers.assignments_grading_put_operation_description,
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description=swaggers.assignments_grading_patch_operation_description,
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class AnnouncementListCreateView(generics.ListCreateAPIView):
    pagination_class = PostListPagination
    permission_classes = [IsAdmin | (IsAuthenticated & IsQualified & IsProfessorOrReadOnly)]
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(lecture_id=self.kwargs['pk']).filter(is_announcement=True)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['lecture_id'] = self.kwargs['pk']
        return context

    @swagger_auto_schema(
        operation_description=swaggers.class_announcements_get_operation_description,
        responses=swaggers.class_announcements_get_responses,
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description=swaggers.class_announcements_post_operation_description,
        request_body=swaggers.class_announcements_post_request_body,
        responses=swaggers.class_announcements_post_responses,
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class AnnouncementDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdmin | (IsAuthenticated & IsQualified & IsCreatorReadOnly)]
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer

    @swagger_auto_schema(
        operation_description=swaggers.announcement_get_operation_description,
        responses=swaggers.announcement_get_responses,
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description=swaggers.announcement_patch_operation_description,
        request_body=swaggers.announcement_patch_request_body,
        responses=swaggers.announcement_patch_responses,
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description=swaggers.announcement_delete_operation_description,
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class QuestionListCreateView(generics.ListCreateAPIView):
    pagination_class = PostListPagination
    permission_classes = [IsAdmin | (IsAuthenticated & IsQualified)]
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(lecture_id=self.kwargs['pk']).filter(is_announcement=False)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['lecture_id'] = self.kwargs['pk']
        return context

    @swagger_auto_schema(
        operation_description=swaggers.class_questions_get_operation_description,
        responses=swaggers.class_questions_get_responses,
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description=swaggers.class_questions_post_operation_description,
        request_body=swaggers.class_questions_post_request_body,
        responses=swaggers.class_questions_post_responses,
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdmin | (IsAuthenticated & IsQualified & (IsProfessor | IsCreatorReadOnly))]
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer

    @swagger_auto_schema(
        operation_description=swaggers.question_get_operation_description,
        responses=swaggers.question_get_responses,
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description=swaggers.question_patch_operation_description,
        request_body=swaggers.question_patch_request_body,
        responses=swaggers.question_patch_responses,
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description=swaggers.question_delete_operation_description,
    )
    def delete(self, request, *args, **kwargs):

        return super().delete(request, *args, **kwargs)


class CommentCreateView(generics.CreateAPIView):
    permission_classes = [IsAdmin | (IsAuthenticated & IsQualified)]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['post_id'] = self.kwargs['pk']
        return context

    @swagger_auto_schema(
        operation_description=swaggers.post_comments_post_operation_description,
        request_body=swaggers.post_comments_post_request_body,
        responses=swaggers.post_comments_post_responses,
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdmin | (IsAuthenticated & IsQualified & (IsProfessorOrReadOnly | IsCreatorReadOnly))]
    serializer_class = CommentDetailSerializer
    queryset = Comment.objects.all()

    @swagger_auto_schema(
        operation_description=swaggers.comment_get_operation_description,
        responses=swaggers.comment_get_responses,
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description=swaggers.comment_patch_operation_description,
        request_body=swaggers.comment_patch_request_body,
        responses=swaggers.comment_patch_responses,
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description=swaggers.comment_delete_operation_description,
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class AssignmentUploadView(views.APIView):
    parser_classes = [MultiPartParser, ]
    permission_classes = [IsQualified]

    @swagger_auto_schema(
        operation_description=swaggers.assignments_upload_put_operation_description,
        request_body=AssignmentFileSerializer
    )
    def put(self, request, pk, format=None):
        if 'file' not in request.data:
            Response(status=status.HTTP_400_BAD_REQUEST)
        file_obj = request.data.get('file', None)
        obj = AssignmentToStudent.objects.get(assignment=pk, student=self.request.user)
        obj.file.save(file_obj.name, file_obj, save=True)
        obj.is_submitted = True
        obj.save()
        return Response(status=status.HTTP_201_CREATED)


class AssignmentDownloadView(generics.RetrieveAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentFileSerializer
    permission_classes = [IsQualified]

    @swagger_auto_schema(operation_description=swaggers.assignments_download_get_operation_description)
    def get(self, request, *args, **kwargs):
        instance = AssignmentToStudent.objects.get(assignment=self.kwargs['pk'], student=self.request.user)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class AssignmentDownloadByUserIDView(generics.RetrieveAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentFileSerializer
    permission_classes = [IsCreatorReadOnly]

    @swagger_auto_schema(operation_description=swaggers.assignments_user_download_get_operation_description)
    def get(self, request, *args, **kwargs):
        instance = AssignmentToStudent.objects.get(assignment=self.kwargs['pk'], student=self.kwargs['user_pk'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class AssignmentGradeListView(generics.ListAPIView):
    serializer_class = AssignmentToStudentSerializer
    permission_classes = [IsQualified]
    def get_queryset(self):
        assignments = Assignment.objects.all().filter(lecture=self.kwargs['pk'])
        query = []
        for i in assignments:
            query.append(AssignmentToStudent.objects.get(assignment=i,student=self.request.user))
        return query

    @swagger_auto_schema(
        operation_description=swaggers.assignments_class_total_get_operation_description
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)