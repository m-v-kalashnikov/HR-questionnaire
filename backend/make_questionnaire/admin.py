from django.contrib import admin
from .models import \
    Answer, \
    QuestionInQuestionnaire, \
    Question, \
    Questionnaire, \
    UserAnswer

admin.site.register(Answer)

admin.site.register(QuestionInQuestionnaire)

admin.site.register(Question)

admin.site.register(Questionnaire)

admin.site.register(UserAnswer)
