from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from django_filters import rest_framework as filters

from .models import (Answer, Question, QuestionInQuestionnaire, Questionnaire,
                     UserAnswer)
from .serializers import (AnswerSerializer, AnswerWithCorrectSerializer,
                          QuestionInQuestionnaireSerializer,
                          QuestionInQuestionnaireWithCorrectSerializer,
                          QuestionnaireSerializer, QuestionSerializer,
                          QuestionWithCorrectSerializer, UserAnswerSerializer,
                          StatisticsUserAnswerSerializer, StatisticsUserSerializer)
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from accounts.models import User


class QuestionnaireViewSet(viewsets.ModelViewSet):
    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated]


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]


class AnswerWithCorrectViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerWithCorrectSerializer
    permission_classes = [IsAuthenticated]


class QuestionInQuestionnaireViewSet(viewsets.ModelViewSet):
    queryset = QuestionInQuestionnaire.objects.all()
    serializer_class = QuestionInQuestionnaireSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('questionnaire__slug',)
    permission_classes = [IsAuthenticated]


class QuestionInQuestionnaireWithCorrectViewSet(viewsets.ModelViewSet):
    queryset = QuestionInQuestionnaire.objects.all()
    serializer_class = QuestionInQuestionnaireWithCorrectSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('questionnaire__slug',)
    permission_classes = [IsAuthenticated]


class QuestionWithCorrectViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionWithCorrectSerializer
    permission_classes = [IsAuthenticated]


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        title = request.data['title']
        image = request.data['image']
        if image:
            Question.objects.create(title=title, image=image)
        else:
            Question.objects.create(title=title)
        return HttpResponse({'massage': 'Question created'}, status=200)


class UserAnswerViewSet(viewsets.ModelViewSet):
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = (
        'question_in_questionnaire__questionnaire__slug', 'user_profile')
    permission_classes = [IsAuthenticated]


class StatisticsUserAnswerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserAnswer.objects.all()
    serializer_class = StatisticsUserAnswerSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = (
        'question_in_questionnaire__questionnaire__slug', 'user_profile')
    permission_classes = [IsAuthenticated]


class StatisticsUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = StatisticsUserSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('id',)
    permission_classes = [IsAuthenticated]
