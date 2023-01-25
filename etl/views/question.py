from etl.serializers import *
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from etl.models import *
from etl.permissions import *
from etl.paginations import *
from drf_yasg.utils import swagger_auto_schema
import etl.swaggers as swaggers


class QuestionListCreateView(generics.ListCreateAPIView):
    pagination_class = PostListPagination
    permission_classes = [IsAdmin | (IsAuthenticated & IsQualified)]
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(lecture_id=self.kwargs['pk']).filter(is_announcement=False)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['lecture_id'] = self.kwargs['pk']
        context['is_announcement'] = False
        return context

    @swagger_auto_schema(
        operation_description=swaggers.class_questions_get_operation_description,
        responses=swaggers.class_questions_get_responses,
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description=swaggers.class_questions_post_operation_description,
        request_body=swaggers.class_questions_post_request_body,
        responses=swaggers.class_questions_post_responses,
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdmin | (IsAuthenticated & IsQualified & (IsProfessor | IsCreatorReadOnly))]
    serializer_class = PostDetailSerializer

    def get_queryset(self):
        return Post.objects.filter(is_announcement=False)

    @swagger_auto_schema(
        operation_description=swaggers.question_get_operation_description,
        responses=swaggers.question_get_responses,
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description=swaggers.question_patch_operation_description,
        request_body=swaggers.question_patch_request_body,
        responses=swaggers.question_patch_responses,
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description=swaggers.question_delete_operation_description,
    )
    def delete(self, request, *args, **kwargs):

        return super().delete(request, *args, **kwargs)


class QuestionSearchView(generics.ListAPIView):
    permission_classes = [IsAdmin | (IsAuthenticated & IsQualified)]
    serializer_class = PostSerializer
    pagination_class = PostListPagination

    # TODO: 현재는 제목 검색만 구현되어 있음.
    def get_queryset(self):
        question_name = self.request.GET['name']
        return Post.objects.filter(is_announcement=False)\
            .filter(lecture_id=self.kwargs['pk'])\
            .filter(title__contains=question_name)

    @swagger_auto_schema(
        operation_description=swaggers.class_questions_search_operation_description,
        responses=swaggers.class_questions_search_responses,
        manual_parameters=swaggers.class_questions_search_manual_parameters,
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
