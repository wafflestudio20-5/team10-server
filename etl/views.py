from authentication.serializers import UserLoginSerializer
from .serializers import *
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from .models import *
from .permissions import *
from .paginations import *
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
import etl.swaggers as swaggers


class ClassListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdmin | (IsAuthenticated & IsProfessorOrReadOnly)]
    queryset = Class.objects.all()
    serializer_class = ClassSerializer


class ProfessorClassListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdmin | (IsAuthenticated & IsQualified & IsProfessor)]
    serializer_class = ClassSerializer

    def get_queryset(self):
        return Class.objects.filter(created_by=self.request.user)


class ClassDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAdmin | IsCreatorReadOnly]
    queryset = Class.objects.all()


class EnrollClassView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated & IsQualified]
    serializer_class = EnrollDropSerializer

    @swagger_auto_schema(
        request_body=swaggers.enroll_request_body,
        responses=swaggers.enroll_responses,
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
    permission_classes = [IsAuthenticated & IsQualified]
    serializer_class = EnrollDropSerializer

    @swagger_auto_schema(
        request_body=swaggers.drop_request_body,
        responses=swaggers.drop_responses,
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


# GET assignments/
# 모든 assignments list 반환
class AssignmentListCreateView(generics.ListCreateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentCreateSerializer
    permission_classes = [IsProfessorOrReadOnly | IsAdmin]

    @swagger_auto_schema(operation_description="Assignment 생성 : 교수자가 Class id, 과제 name, due date, 최대 점수, 가중치 입력")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Assignment list : 존재하는 모든 class의 모든 Assignment List 반환")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)



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

    @swagger_auto_schema(operation_description="Assignment Detail : id번째 Assignment의 정보 반환")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Assignment 수정 : 교수자가 id번째 Assignment의 Class id, 과제 name, due date, 최대 점수, 가중치 모두 입력해 수정")
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Assignment 수정 : 교수자가 id번째 Assignment의 Class id, 과제 name, due date, 최대 점수, 가중치 중 일부 입력해 수정")
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Assignment 삭제 : 교수자가 id번째 Assignment 삭제")
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


# GET assignments/class/<int:pk>/
# pk번째 class의 모든 assignment list 반환
class AssignmentListByLectureView(generics.ListAPIView):
    serializer_class = AssignmentCreateSerializer
    permission_classes = [IsQualified]

    def get_queryset(self):
        return Assignment.objects.all().filter(lecture=self.kwargs['pk'])

    @swagger_auto_schema(operation_description="Assignment list By Lecture : id번째 Class의 모든 Assignment List 반환")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

# GET assignments/student/
# 학생이 자신의 모든 assignment list 반환
class AssignmentListByStudentView(generics.ListAPIView):
    serializer_class = AssignmentCreateSerializer
    permission_classes = [IsQualified]

    def get_queryset(self):
        return Assignment.objects.all().filter(student=self.request.user)

    @swagger_auto_schema(operation_description="Assignment list By Student : 로그인 한 User의 모든 Assignment List 반환")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


# GET assignments/grade/<int:pk>/
# 학생이 pk번째 assignment 점수, 제출여부, 채점여부 확인
class AssignmentGradeGetView(generics.RetrieveAPIView):
    serializer_class = AssignmentToStudentSerializer
    permission_classes = [IsQualified]

    @swagger_auto_schema(operation_description="Get Assignment Grade : 로그인 한 User의 id번째 Assignment의 채점 정보 반환(is_submited, is_graded, score)")
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

    @swagger_auto_schema(operation_description="Assignment 채점 : 교수자가 id번째 Assignment의 성적을 해당 학생의 user_id, 점수를 입력해 채점")
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Assignment 채점 : 교수자가 id번째 Assignment의 성적을 해당 학생의 user_id, 점수를 입력해 채점")
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


# 디버깅용 모든 유저의 정보를 보는 View
# class UserListView(generics.ListAPIView):
#     permission_classes = [IsAdmin]
#     queryset = User.objects.all()
#     serializer_class = UserDetailSerializer
