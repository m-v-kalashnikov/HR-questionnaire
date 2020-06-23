import q
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import UserProfile
from .permissions import IsOwnerProfileOrReadOnly
from .serializers import UserProfileSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsOwnerProfileOrReadOnly, IsAuthenticated]


@api_view(('GET',))
def user_info(request):
    user_id = request.user.id
    user = get_object_or_404(User, id=user_id)

    return JsonResponse({
        'id': user_id,
        'username': user.username,
        'email': user.email,
        'description': user.profile.description,
        'is_superuser': user.is_superuser,
        'is_staff': user.is_staff,
        'want_to_be_manager': user.profile.want_to_be_manager,
    })
