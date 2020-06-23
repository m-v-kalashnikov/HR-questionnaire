from django.urls import re_path
from rest_framework import routers
from accounts.views import UserProfileViewSet, user_info

app_name = 'accounts'

router = routers.DefaultRouter()
router.register(r'profile', UserProfileViewSet, basename='accounts')

urlpatterns = router.urls

urlpatterns += [
    re_path(r'^current_user_info/', user_info, name='current_user_info')]
