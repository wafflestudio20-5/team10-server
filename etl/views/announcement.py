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

    def __init__(self):
        super().__init__()
        self.total_count = 0

    def get_queryset(self):
        queryset = Post.objects.filter(lecture_id=self.kwargs['pk']).filter(is_announcement=True).order_by('-created_at')
        self.total_count = queryset.count()
        return queryset

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
        get_data = super().get(request, *args, **kwargs)
        # OrderedDict 타입인 .data에 접근하여 response를 조작할 수 있음.
        get_data.data['total_announcement_count'] = self.total_count
        return get_data

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
        next = self.get_queryset().filter(pk__gt=self.kwargs['pk']).order_by('pk').first()
        prev = self.get_queryset().filter(pk__lt=self.kwargs['pk']).order_by('pk').last()
        next_serializer = AnnouncementSerializer(next)
        prev_serializer = AnnouncementSerializer(prev)

        announ = Post.objects.get(id=self.kwargs['pk'])
        announ.hits += 1
        announ.save()

        data = {
            'post_info': super().get(request, *args, **kwargs),
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


class AnnouncementSearchView(generics.ListAPIView):
    permission_classes = [IsAdmin | (IsAuthenticated & IsQualified)]
    serializer_class = AnnouncementSerializer
    pagination_class = PostListPagination

    def __init__(self):
        super().__init__()
        self.total_count = 0

    # TODO: 현재는 제목 검색만으로 구현해 놓았는데 내용 검색도 필요한가??
    def get_queryset(self):
        announcement_name = self.request.GET['name']
        queryset = Post.objects.filter(is_announcement=True)\
            .filter(lecture_id=self.kwargs['pk'])\
            .filter(title__contains=announcement_name)\
            .order_by('-created_at')
        self.total_count = queryset.count()
        return queryset

    @swagger_auto_schema(
        operation_description=swaggers.class_announcements_search_operation_description,
        responses=swaggers.class_announcements_search_responses,
        manual_parameters=swaggers.class_announcements_search_manual_parameters,
    )
    def get(self, request, *args, **kwargs):
        get_data = super().get(request, *args, **kwargs)
        get_data.data['total_announcement_count'] = self.total_count
        return get_data
