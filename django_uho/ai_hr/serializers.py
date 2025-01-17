from rest_framework import serializers
from .models import Candidate, JobCriteria, InterviewStage

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'

class JobCriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCriteria
        fields = '__all__'

class InterviewStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewStage
        fields = '__all__'
