from django.db import models


class Answer(models.Model):
    title = models.TextField('Описание', null=True)
    question = models.ForeignKey('Question',
                                 related_name='answer',
                                 on_delete=models.SET_NULL,
                                 null=True
                                 )
    correct = models.NullBooleanField('Верен ли ответ')

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
        answer = self.title
        if len(answer) > 10:
            answer = '{}...'.format(answer[0:10])
        return '{question} -- {answer}'.format(answer=answer, question=self.question)
