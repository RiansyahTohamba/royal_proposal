
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Candidate
from .serializers import CandidateSerializer

class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    @action(detail=True, methods=['get'])
    def get_candidate(self):
        return Response(candidates=[],status=status.HTTP_200_OK)

    # @action(detail=True, methods=['post'])
    # def upload_cv(self, request, pk=None):
    #     candidate = self.get_object()
    #     candidate.cv = request.data['cv']
    #     candidate.save()
    #     return Response(status=status.HTTP_200_OK)
