from rest_framework import serializers
from .models import \
    Answer, \
    QuestionInQuestionnaire, \
    Question, \
    Questionnaire, \
    UserAnswer


class QuestionnaireSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='make_questionnaire_app:questionnaire-detail',
        lookup_field='slug'
    )
    questionnaire_type = serializers.CharField(source='get_questionnaire_type_display')

    class Meta:
        model = Questionnaire
        fields = ['url', 'title', 'questionnaire_type', 'description']


class AnswerSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='make_questionnaire_app:answer-detail',
    )
    question = serializers.StringRelatedField(read_only=True)  # TODO: make it serializer

    class Meta:
        model = Answer
        fields = ['url', 'title', 'question', 'correct']


class QuestionInQuestionnaireSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='make_questionnaire_app:question_in_questionnaire-detail',
    #     lookup_field='id'
    )
    question = serializers.StringRelatedField(read_only=True) # TODO: make it serializer
    questionnaire = serializers.StringRelatedField(read_only=True) # TODO: make it serializer

    class Meta:
        model = QuestionInQuestionnaire
        fields = ['url', 'question', 'questionnaire', 'value']


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='make_questionnaire_app:question-detail',
    )

    class Meta:
        model = Question
        fields = ['url', 'title', 'image']


class UserAnswerSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='make_questionnaire_app:user_answer-detail',
    )
    question_in_questionnaire = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = UserAnswer
        fields = ['url', 'user_profile', 'question_in_questionnaire', 'answer']



