"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os

from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from accounts.views import CustomTokenObtainPairView

urlpatterns = [
    path('api/accounts/', include('accounts.urls', namespace="accounts")),
    path('auth/jwt/token/', CustomTokenObtainPairView.as_view(), name='custom_token_obtain_pair'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('api/{}/'.format(os.getenv('ADMIN_PANEL_URL')), admin.site.urls),
    path('api/', include('make_questionnaire.urls', namespace="make_questionnaire_app")),
    path('tinymce/', include('tinymce.urls')),
]
if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
