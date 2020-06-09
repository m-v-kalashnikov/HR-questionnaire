from rest_framework import routers
from .views import \
    QuestionnaireViewSet, \
    AnswerViewSet, \
    QuestionInQuestionnaireViewSet, \
    QuestionViewSet, \
    UserAnswerViewSet

app_name = 'make_questionnaire_app'

router = routers.DefaultRouter()
router.register(r'questionnaire', QuestionnaireViewSet, basename='questionnaire')
router.register(r'answer', AnswerViewSet, basename='answer')
router.register(r'question-in-questionnaire', QuestionInQuestionnaireViewSet, basename='question_in_questionnaire')
router.register(r'question', QuestionViewSet, basename='question')
router.register(r'user-answer', UserAnswerViewSet, basename='user_answer')


urlpatterns = router.urls
