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


# GET assignments/
# 모든 assignments list 반환
class AssignmentListCreateView(generics.ListCreateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentCreateSerializer
    permission_classes = [IsProfessorOrReadOnly | IsAdmin]


# GET, PUT, PATCH, DELETE assignments/<int:pk>/
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


# GET assignments/class/<int:pk>/
# pk번째 class의 모든 assignment list 반환
class AssignmentListByLectureView(generics.ListAPIView):
    serializer_class = AssignmentCreateSerializer
    permission_classes = [IsQualified]

    def get_queryset(self):
        return Assignment.objects.all().filter(lecture=self.kwargs['pk'])


# GET assignments/student/
# 학생이 자신의 모든 assignment list 반환
class AssignmentListByStudentView(generics.ListAPIView):
    serializer_class = AssignmentCreateSerializer
    permission_classes = [IsQualified]

    def get_queryset(self):
        return Assignment.objects.all().filter(student=self.request.user)


# GET assignments/grade/<int:pk>/
# 학생이 pk번째 assignment 점수, 제출여부, 채점여부 확인
class AssignmentGradeGetView(generics.RetrieveAPIView):
    serializer_class = AssignmentToStudentSerializer
    permission_classes = [IsQualified]

    def get(self, request, *args, **kwargs):
        obj = AssignmentToStudent.objects.get(assignment=self.kwargs['pk'], student=self.request.user)
        serializer = AssignmentToStudentSerializer(obj)
        return Response(serializer.data)


# PUT(PATCH) assignments/grading/<int:pk>/
# 교수자가 pk번째 assignments 채점. 학번, 점수 입력
class AssignmentGradingView(generics.UpdateAPIView):
    queryset = Assignment.objects.all()
    serializer_class=AssignmentGradingSerializer
    permission_classes = [IsCreatorReadOnly | IsAdmin]
