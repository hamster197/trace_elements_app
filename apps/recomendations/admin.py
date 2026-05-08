from django.contrib import admin

from apps.recomendations.models import RecomendationResult, RecomendationDiscription, NutritionComposition, \
    NutritionQuide


# Register your models here.


class NutritionCompositionInlineAdmin(admin.StackedInline):
    model = NutritionComposition

@admin.register(NutritionQuide)
class NutritionQuideModelAdmin(admin.ModelAdmin):
    list_display=('pk', 'elements_id', 'man', 'age_min', 'age_max')

@admin.register(RecomendationResult)
class RecomendationResultModelAdmin(admin.ModelAdmin):
    list_display=('pk', 'user_id', 'creation_date',)

    # def has_change_permission(self, request, obj=None):
    #     return False



@admin.register(RecomendationDiscription)
class RecomendationDiscriptionModelAdmin(admin.ModelAdmin):
    list_display=('pk', 'imt_min', 'imt_max', 'title',)
    inlines = (NutritionCompositionInlineAdmin, )

