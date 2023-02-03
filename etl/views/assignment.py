from etl.serializers import *
from rest_framework import generics, status, views
from etl.models import *
from etl.permissions import *
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
import etl.swaggers as swaggers
from rest_framework.parsers import MultiPartParser


# 모든 assignments list 반환
class AssignmentListCreateView(generics.ListCreateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentCreateSerializer
    permission_classes = (IsAdminOrProfessorOrReadOnly,)

    @swagger_auto_schema(
        operation_description=swaggers.assignments_get_operation_description,
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description=swaggers.assignments_post_operation_description,
        request_body=swaggers.assignments_post_request_body,
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


# pk번째 assignments detail 반환, 수정, 삭제
class AssignmentClassView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentDetailSerializer
    permission_classes = (IsAdminOrCreatorOrReadOnly,)

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
    permission_classes = (IsAdminOrQualified,)

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
    permission_classes = (IsAdminOrQualified,)

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
    permission_classes = (IsAdminOrQualified,)

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
    permission_classes = (IsAdminOrCreatorOrReadOnly,)

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


class AssignmentUploadView(views.APIView):
    parser_classes = [MultiPartParser, ]
    permission_classes = (IsAdminOrQualified,)

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
    permission_classes = (IsAdminOrQualified,)

    @swagger_auto_schema(operation_description=swaggers.assignments_download_get_operation_description)
    def get(self, request, *args, **kwargs):
        instance = AssignmentToStudent.objects.get(assignment=self.kwargs['pk'], student=self.request.user)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class AssignmentDownloadByUserIDView(generics.RetrieveAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentFileSerializer
    permission_classes = (IsAdminOrCreatorOrReadOnly,)

    @swagger_auto_schema(operation_description=swaggers.assignments_user_download_get_operation_description)
    def get(self, request, *args, **kwargs):
        instance = AssignmentToStudent.objects.get(assignment=self.kwargs['pk'], student=self.kwargs['user_pk'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class AssignmentGradeListView(generics.ListAPIView):
    serializer_class = AssignmentToStudentSerializer
    permission_classes = (IsAdminOrQualified,)

    def get_queryset(self):
        assignments = Assignment.objects.all().filter(lecture=self.kwargs['pk'])
        query = []
        for i in assignments:
            query.append(AssignmentToStudent.objects.get(assignment=i, student=self.request.user))
        return query

    @swagger_auto_schema(
        operation_description=swaggers.assignments_class_total_get_operation_description
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
