from rest_framework import serializers
from .models import Questionnaire, QuestionInQuestionnaire, Question, Answer, UserAnswer
from accounts.models import User


class QuestionnaireSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='make_questionnaire_app:questionnaire-detail',
        lookup_field='slug'
    )

    class Meta:
        model = Questionnaire
        fields = ['url', 'title', 'questionnaire_type', 'when_to_start', 'description', 'slug']


class AnswerSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='make_questionnaire_app:answer-detail',
    )

    class Meta:
        model = Answer
        fields = ['url', 'id', 'title']


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='make_questionnaire_app:question-detail',
    )
    answer = AnswerSerializer(many=True, allow_null=True)

    class Meta:
        model = Question
        fields = ['url', 'id', 'title', 'image', 'answer']


class QuestionInQuestionnaireSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='make_questionnaire_app:question_in_questionnaire-detail',
    )
    question = QuestionSerializer(read_only=True)
    questionnaire = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug'
    )

    class Meta:
        model = QuestionInQuestionnaire
        fields = ['url', 'id', 'question', 'questionnaire', 'value', 'multi_correct']


class UserAnswerSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='make_questionnaire_app:user_answer-detail',
    )
    question_in_questionnaire = serializers.PrimaryKeyRelatedField(queryset=QuestionInQuestionnaire.objects.all())
    answer = serializers.PrimaryKeyRelatedField(many=True, queryset=Answer.objects.all())
    user_profile = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = UserAnswer
        fields = ['url', 'id', 'user_profile', 'string_answer', 'question_in_questionnaire', 'answer', 'questionnaire_slug']
