from django.db import models
from django.contrib.auth.models import User


class UserAnswer(models.Model):
    user = models.ForeignKey(User,
                             related_name='user_answer',
                             on_delete=models.SET_NULL,
                             null=True
                             )
    question_in_questionnaire = models.ForeignKey('QuestionInQuestionnaire',
                                                  related_name='user_answer',
                                                  on_delete=models.SET_NULL,
                                                  null=True
                                                  )
    answer = models.ManyToManyField('Answer',
                                    related_name='user_answer',
                                    blank=True
                                    )

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = 'Ответ пользователя'
        verbose_name_plural = 'Ответы пользователей'

    def __str__(self):
        answer = self.answer
        user = self.user
        question_in_questionnaire = self.question_in_questionnaire
        return '{answer} пользователя {user} на {question_in_questionnaire}'.format(
            answer=answer,
            user=user,
            question_in_questionnaire=question_in_questionnaire
        )
