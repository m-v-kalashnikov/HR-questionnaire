from rest_framework import routers
from accounts.views import UserProfileViewSet

app_name = 'accounts'

router = routers.DefaultRouter()
router.register(r'profile', UserProfileViewSet, basename='accounts')

urlpatterns = router.urls
