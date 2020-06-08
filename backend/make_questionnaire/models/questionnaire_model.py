import itertools
from django.db import models
from django.utils.text import slugify
from googletrans import Translator
from django.utils.translation import gettext_lazy as _


class Questionnaire(models.Model):
    class QuestionnaireType(models.TextChoices):
        QUESTIONS = 'QS', _('Опросник')
        TESTS = 'TS', _('Тесты')

    title = models.CharField('Название', max_length=128)
    questionnaire_type = models.CharField('Тип вопросов',
                                          max_length=2,
                                          choices=QuestionnaireType.choices,
                                          default=QuestionnaireType.QUESTIONS,
                                          )
    description = models.CharField('Описание', max_length=512, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    slug = models.SlugField(default='',
                            editable=False,
                            max_length=256,
                            )

    class Meta:
        verbose_name = 'Опросник'
        verbose_name_plural = 'Опросники'

    def __str__(self):
        return self.title

    def _generate_slug(self):
        value = Translator().translate('{}'.format(self.title), dest='en').text
        slug_candidate = slug_original = slugify(value, allow_unicode=True)
        for i in itertools.count(1):
            if not Questionnaire.objects.filter(slug=slug_candidate).exists():
                break
            slug_candidate = '{}-{}'.format(slug_original, i)

        self.slug = slug_candidate

    def save(self, *args, **kwargs):
        if not self.pk:
            self._generate_slug()

        super().save(*args, **kwargs)
