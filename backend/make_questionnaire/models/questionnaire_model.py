import datetime
import itertools
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from googletrans import Translator
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField


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
    when_to_start = models.DateTimeField('Когда можно проходить', null=True)
    description = HTMLField('Описание', null=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True, null=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True, null=True)
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

    def was_published_recently(self):
        return self.created_at >= timezone.now() - datetime.timedelta(days=1)

    was_published_recently.admin_order_field = 'created_at'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Было ли создано недавно?'
