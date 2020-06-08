from django.db import models


def user_directory_path(filename):
    return 'question/{filename}/'.format(filename=filename)

class Question(models.Model):
    title = models.TextField('Описание', null=True)
    image = models.ImageField('Изображение',
                              upload_to='question/',
                              null=True,
                              blank=True
                              )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        question = self.title
        if len(question) > 20:
            question = '{}...'.format(question[0:20])
        return question
