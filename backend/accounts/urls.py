from django.urls import path, re_path, include

from accounts.views import user_info

urlpatterns = [
    re_path(r'^current_user_info/', user_info),
    re_path(r'^auth/', include('rest_auth.urls')),
    re_path(r'^registration/', include('rest_auth.registration.urls')),
]
