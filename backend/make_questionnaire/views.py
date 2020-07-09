from django.http import HttpResponse
from rest_framework import viewsets
from django_filters import rest_framework as filters
from .models import Questionnaire, QuestionInQuestionnaire, UserAnswer, Question, Answer
from .serializers import QuestionnaireSerializer, QuestionInQuestionnaireSerializer, UserAnswerSerializer, \
    QuestionSerializer, AnswerSerializer, QuestionInQuestionnaireWithCorrectSerializer, QuestionWithCorrectSerializer, \
    AnswerWithCorrectSerializer


class QuestionnaireViewSet(viewsets.ModelViewSet):
    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireSerializer
    lookup_field = 'slug'
    # TODO: only admin/manager can make changes


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    # TODO: 1) only admin/manager can make changes 2) only authenticated


class AnswerWithCorrectViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerWithCorrectSerializer
    # TODO: 1) only admin/manager can make changes 2) only authenticated


class QuestionInQuestionnaireViewSet(viewsets.ModelViewSet):
    queryset = QuestionInQuestionnaire.objects.all()
    serializer_class = QuestionInQuestionnaireSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('questionnaire__slug',)
    # TODO: 1) only authenticated


class QuestionInQuestionnaireWithCorrectViewSet(viewsets.ModelViewSet):
    queryset = QuestionInQuestionnaire.objects.all()
    serializer_class = QuestionInQuestionnaireWithCorrectSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('questionnaire__slug',)
    # TODO: 1) only authenticated


class QuestionWithCorrectViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionWithCorrectSerializer


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
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('question_in_questionnaire__questionnaire__slug', 'user_profile')
    # TODO: 1) only admin/manager can make changes 2) only authenticated

