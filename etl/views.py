from .serializers import *
from rest_framework import generics, permissions
from .models import *
from authentication.serializers import UserSerializer
from .permissions import *


class ClassListView(generics.ListAPIView):
    permission_classes = [IsQualified]
    queryset = Class.objects.all()
    serializer_class = ClassSerializer


class ClassCreateView(generics.CreateAPIView):
    permission_classes = [IsProfessorOrReadOnly]
    serializer_class = ClassSerializer


# 수강신청에 사용하는 클래스. 수강신청 후 다시 유저정보를 불러와야 하므로 GET 요청으로 처리함.
class EnrollClassView(generics.RetrieveAPIView):
    permission_classes = [DoesUserMatchRequest]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get(self, *args, **kwargs):
        # url 형식을 'etl/<int:pk>/enroll/?class_id={클래스 아이디}' 형식으로, class_id를 패러미터로 받기 때문에 이를 parsing
        class_id = int(self.request.GET['class_id'])
        lecture = Class.objects.get(id=class_id)
        # 아래 코드가 이해되지 않는다면 models.py의 Class model 참조 바람.
        self.request.user.classes.add(lecture)
        return super().get(self, *args, **kwargs)


# 수업 드랍에 사용하는 클래스. 드랍 후 다시 유저정보를 불러와야 하므로 GET 요청으로 처리함.
class DropClassView(generics.RetrieveAPIView):
    permission_classes = [DoesUserMatchRequest]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    # 코드에 대한 설명은 EnrollClassView 와 유사하므로 이를 참조하기 바람.
    def get(self, *args, **kwargs):
        class_id = int(self.request.GET['class_id'])
        lecture = Class.objects.get(id=class_id)
        self.request.user.classes.remove(lecture)
        return super().get(self, *args, **kwargs)
