from django.contrib import admin

from apps.questionnaire.models import *

# Register your models here.

admin.site.register(LoadIntensityQuide)
admin.site.register(TypeOfActivityQuide)

@admin.register(Questionnaire)
class QuestionnaireModelAdmin(admin.ModelAdmin):
    list_display=('pk', 'user_id', 'creation_date',)
    search_fields = ('user_id',)

@admin.register(QuizeResult)
class QuizeResulteModelAdmin(admin.ModelAdmin):
    list_display=('pk', 'user_id', 'creation_date',)

@admin.register(QuizeResultElement)
class QuizeResultElementModelAdmin(admin.ModelAdmin):
    list_display=('pk', 'quize_id', 'element_id', 'estimation')

@admin.register(QuestionQuide)
class QuestionQuideModelAdmin(admin.ModelAdmin):
    list_display=('pk', 'get_elements', 'text',)

    def get_elements(self, obj):
        return ", ".join([element.title for element in obj.elements_id.all()])
