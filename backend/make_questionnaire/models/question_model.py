import datetime
from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField


def user_directory_path(filename):
    return 'question/{filename}/'.format(filename=filename)

class Question(models.Model):
    title = HTMLField('Описание', null=True, blank=True)
    image = models.ImageField('Изображение',
                              upload_to='question/',
                              null=True,
                              blank=True
                              )
    created_at = models.DateTimeField('Создано', auto_now_add=True, null=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True, null=True)

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        question = self.title
        if len(question) > 20:
            question = '{}...'.format(question[0:20])
        return question

    def was_published_recently(self):
        return self.created_at >= timezone.now() - datetime.timedelta(days=1)

    was_published_recently.admin_order_field = 'created_at'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Было ли создано недавно?'
