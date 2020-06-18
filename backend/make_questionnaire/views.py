from django.http import HttpResponse
from rest_framework import viewsets, status
from django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.permissions import IsOwnerProfileOrReadOnly
from .models import \
    Answer, \
    QuestionInQuestionnaire, \
    Question, \
    Questionnaire, \
    UserAnswer

from .serializers import \
    QuestionnaireSerializer, \
    AnswerSerializer, \
    QuestionInQuestionnaireSerializer, \
    QuestionSerializer, \
    UserAnswerSerializer


class QuestionnaireViewSet(viewsets.ModelViewSet):
    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireSerializer
    lookup_field = 'slug'
    # permission_classes = [IsOwnerProfileOrReadOnly] # TODO: only admin/manager can make changes


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsOwnerProfileOrReadOnly] # TODO: 1) only admin/manager can make changes 2) only authenticated


class QuestionInQuestionnaireViewSet(viewsets.ModelViewSet):
    queryset = QuestionInQuestionnaire.objects.all()
    serializer_class = QuestionInQuestionnaireSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('questionnaire__slug',)
    permission_classes = [IsOwnerProfileOrReadOnly] # TODO: 1) only authenticated


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def post(self, request, *args, **kwargs):
        title = request.data['title']
        image = request.data['image']
        if image:
            Question.objects.create(title=title, image=image)
        else:
            Question.objects.create(title=title)
        return HttpResponse({'massage': 'Question created'}, status=200)

    # TODO: 1) only admin/manager can make changes 2) only authenticated


class UserAnswerViewSet(viewsets.ModelViewSet):
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer
    permission_classes = [IsOwnerProfileOrReadOnly] # TODO: 1) only admin/manager can make changes 2) only authenticated
