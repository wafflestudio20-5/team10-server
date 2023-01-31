from etl.serializers import *
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from etl.models import *
from etl.permissions import *
from etl.paginations import *
from drf_yasg.utils import swagger_auto_schema
import etl.swaggers as swaggers
from rest_framework.response import Response
from rest_framework import status


class AnnouncementListCreateView(generics.ListCreateAPIView):
    pagination_class = PostListPagination
    permission_classes = [IsAdmin | (IsAuthenticated & IsQualified & IsProfessorOrReadOnly)]
    serializer_class = AnnouncementSerializer

    def get_queryset(self):
        name = self.request.GET.get('name', '')
        return Post.objects.filter(lecture_id=self.kwargs['pk']).filter(is_announcement=True)\
            .filter(title__contains=name).order_by('-created_at')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['lecture_id'] = self.kwargs['pk']
        return context

    @swagger_auto_schema(
        operation_description=swaggers.class_announcements_get_operation_description,
        responses=swaggers.class_announcements_get_responses,
        manual_parameters=swaggers.class_announcements_get_manual_parameters,
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
    serializer_class = PostDetailSerializer

    def get_queryset(self):
        return Post.objects.filter(is_announcement=True)

    @swagger_auto_schema(
        operation_description=swaggers.announcement_get_operation_description,
        responses=swaggers.announcement_get_responses,
    )
    def get(self, request, *args, **kwargs):
        announ = Post.objects.get(id=self.kwargs['pk'])
        if announ.is_announcement is False:
            return Response(data='Wrong Access', status=status.HTTP_403_FORBIDDEN)
        announ_serializer = self.get_serializer(announ)
        announ.hits += 1
        announ.save()

        next = self.get_queryset().filter(lecture_id=announ.lecture_id).filter(pk__gt=self.kwargs['pk']).order_by('pk').first()
        prev = self.get_queryset().filter(lecture_id=announ.lecture_id).filter(pk__lt=self.kwargs['pk']).order_by('pk').last()
        next_serializer = PostSimpleSerializer(next)
        prev_serializer = PostSimpleSerializer(prev)

        data = {
            'post_info': announ_serializer.data,
            'next_post': next_serializer.data,
            'prev_post': prev_serializer.data
        }

        return Response(data, status=status.HTTP_200_OK)

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
