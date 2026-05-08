from django.contrib import admin

from apps.elements.models import *


# Register your models here.

@admin.register(ElementsQuide)
class ElementsQuideModelAdmin(admin.ModelAdmin):
    list_display=('pk', 'title', 'min_value', 'max_value', 'sex', 'unit',)


# class ElementResultInlineAdmin(admin.StackedInline):
#     model = ElementResult
#
# @admin.register(TestResult)
# class TestResultModelAdmin(admin.ModelAdmin):
#     list_display=('pk', 'author_id', 'creation_date',)
#     search_fields = ('author_id',)
#     inlines = (ElementResultInlineAdmin, )



