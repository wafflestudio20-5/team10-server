from etl.serializers import *
from rest_framework import generics, status, views
from rest_framework.permissions import IsAuthenticated
from etl.models import *
from etl.permissions import *
from etl.paginations import *
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
