from rest_framework import serializers
from .models import Questionnaire


class QuestionnaireSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='make_questionnaire_app:questionnaire-detail',
        lookup_field='slug'
    )
    class Meta:
        model = Questionnaire
        fields = ['url', 'title', 'created_at', 'updated_at']
