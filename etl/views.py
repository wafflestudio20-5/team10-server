from .serializers import *
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from .models import *
from .permissions import *
from .paginations import *
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class ClassListView(generics.ListCreateAPIView):
    permission_classes = [IsAdmin | (IsAuthenticated & IsProfessorOrReadOnly)]
    queryset = Class.objects.all()
    serializer_class = ClassSerializer


class EnrollClassView(generics.CreateAPIView):
    permission_classes = [IsAdmin]
    serializer_class = EnrollDropSerializer

    @swagger_auto_schema(
        request_body=openapi.Schema(
            'Enroll',
            type=openapi.TYPE_OBJECT,
            properties={
                'class_id': openapi.Schema('class id', type=openapi.TYPE_INTEGER),
            },
            description='현재 로그인된 유저가 수강신청할 Class의 id를 입력으로 받습니다.',
        ),
        responses={
            201: openapi.Schema(
                'Enroll',
                description='수강신청 이후 현재 로그인된 유저가 수강하는 Class list를 반환합니다.',
                type=openapi.TYPE_OBJECT,
                properties={
                    'classes': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            'Class',
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema('ID', read_only=True, type=openapi.TYPE_INTEGER),
                                'name': openapi.Schema('name', type=openapi.TYPE_STRING),
                            },
                        ),
                    ),
                }
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        class_id = int(request.data['class_id'])
        lecture = Class.objects.get(id=class_id)
        request.user.classes.add(lecture)
        serializer = EnrollDropSerializer(request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class DropClassView(generics.CreateAPIView):
    permission_classes = [IsAdmin]
    serializer_class = EnrollDropSerializer

    @swagger_auto_schema(
        request_body=openapi.Schema(
            'Drop',
            type=openapi.TYPE_OBJECT,
            properties={
                'class_id': openapi.Schema('class id', type=openapi.TYPE_INTEGER),
            },
            description='현재 로그인된 유저가 수강신청할 Class의 id를 입력으로 받습니다.',
        ),
        responses={
            201: openapi.Schema(
                'Drop',
                description='드랍 이후 현재 로그인된 유저가 수강하는 Class list를 반환합니다.',
                type=openapi.TYPE_OBJECT,
                properties={
                    'classes': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            'Class',
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema('ID', read_only=True, type=openapi.TYPE_INTEGER),
                                'name': openapi.Schema('name', type=openapi.TYPE_STRING),
                            },
                        ),
                    ),
                }
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        class_id = int(request.data['class_id'])
        lecture = Class.objects.get(id=class_id)
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
