from .serializers import *
from rest_framework import generics, permissions
from .models import *


class ClassListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Class.objects.all()
    serializer_class = ClassSerializer


class ClassCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = ClassSerializer
