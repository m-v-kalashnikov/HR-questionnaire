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
    questionnaire_type = serializers.CharField()

    class Meta:
        model = Questionnaire
        fields = ['url', 'slug', 'title', 'when_to_start', 'questionnaire_type', 'description']


class AnswerSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='make_questionnaire_app:answer-detail',
    )

    class Meta:
        model = Answer
        fields = ['url', 'title', 'correct']


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='make_questionnaire_app:question-detail',
    )
    answer = AnswerSerializer(many=True, allow_null=True)

    class Meta:
        model = Question
        fields = ['url', 'title', 'image', 'answer']

    def create(self, validated_data):
        answer_validated_data = validated_data.pop('answer')
        question = Question.objects.create(**validated_data)
        answer_serializer = self.fields['answer']
        for each in answer_validated_data:
            each['question'] = question
        answers = answer_serializer.create(answer_validated_data)
        return question


class QuestionInQuestionnaireSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='make_questionnaire_app:question_in_questionnaire-detail',
    )
    question = QuestionSerializer()
    questionnaire = QuestionnaireSerializer()

    class Meta:
        model = QuestionInQuestionnaire
        fields = ['url', 'question', 'questionnaire', 'value']

    def create(self, validated_data):
        questionnaire_validated_data = validated_data.pop('questionnaire')
        question_validated_data = validated_data.pop('question')
        questionnaire = Questionnaire.objects.get(**questionnaire_validated_data)
        question_serializer = self.fields['question']
        question = question_serializer.create(question_validated_data)
        question_in_questionnaire = QuestionInQuestionnaire.objects.create(question=question, questionnaire=questionnaire, **validated_data)
        return question_in_questionnaire


class UserAnswerSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='make_questionnaire_app:user_answer-detail',
    )
    question_in_questionnaire = QuestionInQuestionnaireSerializer(many=True, read_only=True)

    class Meta:
        model = UserAnswer
        fields = ['url', 'user_profile', 'string_answer', 'question_in_questionnaire', 'answer']
