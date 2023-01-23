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


class AnnouncementListCreateView(generics.ListCreateAPIView):
    pagination_class = PostListPagination
    permission_classes = [IsAdmin | (IsAuthenticated & IsQualified & IsProfessorOrReadOnly)]
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(lecture_id=self.kwargs['pk']).filter(is_announcement=True)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['lecture_id'] = self.kwargs['pk']
        context['is_announcement'] = True
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
