from etl.serializers import *
from rest_framework import generics
from etl.models import *
from etl.permissions import *
from drf_yasg.utils import swagger_auto_schema
import etl.swaggers as swaggers
from rest_framework.parsers import MultiPartParser


# 주차학습 create
class WeeklyCreateView(generics.CreateAPIView):
    serializer_class = WeeklyCreateSerializer
    permission_classes = (IsAdminOrProfessorOrReadOnly,)
    queryset = Weekly.objects.all()

    @swagger_auto_schema(
        operation_description=swaggers.module_weekly_post_operation_description,
        request_body=WeeklyCreateSerializer
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class WeeklyDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WeeklyCreateSerializer
    permission_classes = (IsAdminOrCreatorOrReadOnly,)
    queryset = Weekly.objects.all()


class ModuleContentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ModuleContentCreateSerializer
    permission_classes = (IsAdminOrCreatorOrReadOnly,)
    queryset = ModuleContent.objects.all()
    parser_classes = [MultiPartParser]


class ModuleContentCreateView(generics.CreateAPIView):
    serializer_class = ModuleContentCreateSerializer
    permission_classes = (IsAdminOrProfessorOrReadOnly,)
    queryset = ModuleContent.objects.all()
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_description=swaggers.module_content_post_operation_description,
        request_body=ModuleContentCreateSerializer
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


# module list
class WeeklyModuleByClassView(generics.ListAPIView):
    serializer_class = ModuleSerializer
    permission_classes = (IsAdminOrQualified,)

    def get_queryset(self):
        return Module.objects.all().filter(lecture=self.kwargs['pk'])

    @swagger_auto_schema(
        operation_description=swaggers.module_class_get_operation_description
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
