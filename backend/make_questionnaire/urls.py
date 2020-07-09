from rest_framework import routers
from .views import QuestionnaireViewSet, QuestionInQuestionnaireViewSet, AnswerViewSet, QuestionViewSet, \
    UserAnswerViewSet, QuestionInQuestionnaireWithCorrectViewSet, QuestionWithCorrectViewSet, AnswerWithCorrectViewSet

app_name = 'make_questionnaire_app'

router = routers.DefaultRouter()
router.register(r'questionnaires', QuestionnaireViewSet, basename='questionnaire')
router.register(r'answer', AnswerViewSet, basename='answer')
router.register(r'answer-with-correct', AnswerWithCorrectViewSet, basename='answer_with_correct')
router.register(r'question-in-questionnaire', QuestionInQuestionnaireViewSet, basename='question_in_questionnaire')
router.register(r'question-in-questionnaire-with-correct',
                QuestionInQuestionnaireWithCorrectViewSet,
                basename='question_in_questionnaire_with_correct')
router.register(r'question', QuestionViewSet, basename='question')
router.register(r'question-with-correct', QuestionWithCorrectViewSet, basename='question_with_correct')
router.register(r'user-answer', UserAnswerViewSet, basename='user_answer')

urlpatterns = router.urls
