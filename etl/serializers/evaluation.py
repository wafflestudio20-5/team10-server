from rest_framework import serializers
from etl.models import *

class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassEvaluation
        fields = '__all__'