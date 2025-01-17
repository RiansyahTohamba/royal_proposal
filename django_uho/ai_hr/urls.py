from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CandidateViewSet, JobCriteriaViewSet, InterviewStageViewSet

ai_hr_router = DefaultRouter()
ai_hr_router.register(r'candidates', CandidateViewSet)
ai_hr_router.register(r'job_criteria', JobCriteriaViewSet)
ai_hr_router.register(r'interview_stages', InterviewStageViewSet)

urlpatterns = [
   path('', include(ai_hr_router.urls)),
]