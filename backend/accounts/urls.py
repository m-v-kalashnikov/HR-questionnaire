from django.urls import re_path, include
from rest_framework.routers import DefaultRouter
from .views import user_info, UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = router.urls

urlpatterns += [
    re_path(r'^current_user_info/', user_info),
    re_path(r'^auth/', include('rest_auth.urls')),
    re_path(r'^registration/', include('rest_auth.registration.urls')),
]
