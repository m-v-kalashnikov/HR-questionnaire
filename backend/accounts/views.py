from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from .models import User


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
