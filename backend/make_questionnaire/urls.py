from rest_framework import routers
from .views import QuestionnaireViewSet

app_name = 'make_questionnaire_app'

router = routers.DefaultRouter()
router.register(r'questionnaire', QuestionnaireViewSet, basename='questionnaire')

urlpatterns = router.urls
