from .serializers import *
from rest_framework import generics, permissions
from .models import *
from authentication.serializers import UserSerializer
from .permissions import *
from rest_framework import status
from rest_framework.response import Response


class ClassListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Class.objects.all()
    serializer_class = ClassSerializer


class ClassCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = ClassSerializer


class EnrollClassView(generics.RetrieveAPIView):
    permission_classes = [DoesUserMatchRequest]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get(self, *args, **kwargs):
        class_id = int(self.request.GET['class_id'])
        lecture = Class.objects.get(id=class_id)
        self.request.user.classes.add(lecture)
        return super().get(self, *args, **kwargs)


class DropClassView(generics.RetrieveAPIView):
    permission_classes = [DoesUserMatchRequest]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get(self, *args, **kwargs):
        class_id = int(self.request.GET['class_id'])
        lecture = Class.objects.get(id=class_id)
        self.request.user.classes.remove(lecture)
        return super().get(self, *args, **kwargs)
