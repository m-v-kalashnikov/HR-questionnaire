from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import User
from .permissions import AdminOrMeCanEdit
from .serializers import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = (
        IsAuthenticated,
        AdminOrMeCanEdit,
    )


@api_view(('GET',))
def user_info(request):
    user_id = request.user.id

    user = get_object_or_404(User, id=user_id)

    return JsonResponse({
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'want_to_be_manager': user.want_to_be_manager,
        'is_staff': user.is_staff,
        'is_superuser': user.is_superuser
    })
