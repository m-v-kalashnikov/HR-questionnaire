from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    description = models.TextField('Описание', blank=True, null=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата модификации', auto_now=True)
    is_manager = models.BooleanField('Менеджер', default=False)
    want_to_be_manager = models.BooleanField('Хочет быть менеджером', default=False)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return self.user.username

    def IsManager(self):
        return self.is_manager
