from django.db import models
from accounts.models import UserProfile


class UserAnswer(models.Model):
    user_profile = models.ForeignKey(UserProfile,
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
    string_answer = models.TextField('Ответ', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = 'Ответ пользователя'
        verbose_name_plural = 'Ответы пользователей'

    def __str__(self):
        answer = self.id
        user = self.user_profile
        question_in_questionnaire = self.question_in_questionnaire
        return 'Ответ({answer}) пользователя ({user}) на {question_in_questionnaire}'.format(
            answer=answer,
            user=user,
            question_in_questionnaire=question_in_questionnaire
        )
