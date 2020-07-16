from django.contrib import admin

from .models import \
    Answer, \
    QuestionInQuestionnaire, \
    Question, \
    Questionnaire, \
    UserAnswer

admin.site.register(UserAnswer)


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 3


class QuestionInQuestionnaireInline(admin.TabularInline):
    model = QuestionInQuestionnaire
    extra = 0


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')
    inlines = [AnswerInline]
    fieldsets = [
        (None, {'fields': ['title', 'image']}),
        ('Действия с элементом', {'fields': ['created_at', 'updated_at'], 'classes': ['collapse']}),
    ]
    list_display = ('title', 'created_at', 'was_published_recently')
    list_filter = ['created_at']
    search_fields = ['title']


admin.site.register(Question, QuestionAdmin)


class QuestionnaireAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')
    inlines = [QuestionInQuestionnaireInline]
    fieldsets = [
        (None, {'fields': ['title', 'questionnaire_type', 'when_to_start', 'description']}),
        ('Действия с элементом', {'fields': ['created_at', 'updated_at'], 'classes': ['collapse']}),
    ]
    list_display = ('title', 'created_at', 'was_published_recently')
    list_filter = ['created_at']
    search_fields = ['title']


admin.site.register(Questionnaire, QuestionnaireAdmin)
