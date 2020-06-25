from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    want_to_be_manager = models.BooleanField('Хочет быть менеджером', default=False)
