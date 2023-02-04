from etl.serializers import *
from rest_framework import generics, status
from etl.models import *
from etl.permissions import *
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
import etl.swaggers as swaggers


class IsEvaluatedCheckView(generics.RetrieveAPIView):
    permission_classes = (IsAdminOrQualified,)

    @swagger_auto_schema(
        operation_description=swaggers.evaluation_check_get_description,
    )
    def get(self, request, *args, **kwargs):
        lecture = self.kwargs['pk']
        if ClassEvaluation.objects.filter(lecture=lecture, student=self.request.user).exists():
            return Response({"evaulation": "yes"}, status=status.HTTP_200_OK)
        else:
            return Response({"evaulation": "no"}, status=status.HTTP_404_NOT_FOUND)


class EvaluationView(generics.CreateAPIView):
    permission_classes = (IsAdminOrQualified,)
    serializer_class = EvaluationSerializer
    queryset = ClassEvaluation.objects.all()

    @swagger_auto_schema(
        operation_description=swaggers.evaluation_post_description,
    )
    def post(self, request, *args, **kwargs):
        if not Class.objects.get(pk=self.kwargs['pk']) in self.request.user.classes.all():
            return Response({"not enrolled"}, status=status.HTTP_400_BAD_REQUEST)
        if ClassEvaluation.objects.filter(lecture=Class.objects.get(pk=self.kwargs['pk']), student=self.request.user).exists():
            return Response({"evaluated already"}, status=status.HTTP_400_BAD_REQUEST)
        instance = ClassEvaluation.objects.create(lecture=Class.objects.get(pk=self.kwargs['pk']), student=self.request.user)
        instance.choice_1 = self.request.data['choice_1']
        instance.choice_2 = self.request.data['choice_2']
        instance.choice_3 = self.request.data['choice_3']
        instance.choice_4 = self.request.data['choice_4']
        instance.choice_5 = self.request.data['choice_5']
        instance.choice_6 = self.request.data['choice_6']
        instance.choice_7 = self.request.data['choice_7']
        instance.descriptive_1 = self.request.data['descriptive_1']
        instance.descriptive_2 = self.request.data['descriptive_2']
        instance.save()

        return Response(status=status.HTTP_201_CREATED)
