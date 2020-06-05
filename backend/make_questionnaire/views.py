from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from accounts.permissions import IsOwnerProfileOrReadOnly
from .models import Questionnaire
from .serializers import QuestionnaireSerializer


class QuestionnaireViewSet(viewsets.ModelViewSet):
    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerProfileOrReadOnly, IsAuthenticated]
