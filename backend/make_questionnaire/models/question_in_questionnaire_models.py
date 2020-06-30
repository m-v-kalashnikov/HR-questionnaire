from django.db import models


class QuestionInQuestionnaire(models.Model):
    question = models.ForeignKey('Question',
                                 related_name='question_in_questionnaire',
                                 on_delete=models.SET_NULL,
                                 null=True
                                 )
    questionnaire = models.ForeignKey('Questionnaire',
                                      related_name='question_in_questionnaire',
                                      on_delete=models.SET_NULL,
                                      null=True
                                      )
    value = models.PositiveSmallIntegerField('Ценность правильного ответа',
                                             null=True
                                             )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = 'Вопрос в опросе'
        verbose_name_plural = 'Вопрос в опросе'

    def __str__(self):
        question = self.question.title
        if len(question) > 10:
            question = '{}...'.format(question[0:10])

        questionnaire = self.questionnaire.title
        if len(question) > 10:
            questionnaire = '{}...'.format(questionnaire[0:10])

        return 'Вопрос:({question}) в опросе:({questionaire})'.format(
            question=question,
            questionaire=questionnaire
        )

    def multi_correct(self):
        correct_num = 0
        for answer in self.question.get_answers():
            if answer.correct:
                correct_num += 1
        return correct_num > 1
