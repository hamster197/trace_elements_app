from django.contrib.auth import get_user_model
from django.db import models

from apps.elements.models import ElementsQuide
from apps.questionnaire.models import LoadIntensityQuide


# Create your models here.
class RecomendationResult(models.Model):
    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='recomendation_result_user_id')
    creation_date = models.DateField(auto_now_add=True)
    imt = models.DecimalField('BODY MASS INDEX', max_digits=12, decimal_places=2)
    bmr = models.DecimalField('Basal metabolism', max_digits=11, decimal_places=1)
    KKAL = models.DecimalField('Daily calorie intake', max_digits=12, decimal_places=2)
    load_intensity = models.ForeignKey(LoadIntensityQuide, verbose_name='Intensity of physical activity', on_delete=models.CASCADE,
                                       related_name='recomendation_result_load_intensity_id', )

    class Meta:
        unique_together = ('user_id', 'creation_date')
        ordering = ['-creation_date']
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'creation_date'], name='unique_recomendation_user_id_creation_date', )
        ]

    def clean(self,):
        self.validate_unique()

    def save(self, *args, **kwargs):
        from datetime import datetime
        today = datetime.now().date()
        age = today.year - self.user_id.date_of_birth.year - ((today.month, today.day) < (self.user_id.date_of_birth.month, self.user_id.date_of_birth.day))
        height = self.user_id.questionnaire_user_id.all().first().height / 100
        self.imt = self.user_id.questionnaire_user_id.all().first().weight / (height * height)
        bmr_all = 10 * self.user_id.questionnaire_user_id.all().first().weight + 6.25 * self.user_id.questionnaire_user_id.all().first().height + 5 * age
        if self.user_id.male:
            self.bmr = bmr_all + 5
        else:
            self.bmr = bmr_all - 161
        self.load_intensity = self.user_id.questionnaire_user_id.all().first().load_intensity_id
        from decimal import Decimal
        self.KKAL = Decimal(self.bmr) * self.user_id.questionnaire_user_id.all().first().load_intensity_id.pal

        super(RecomendationResult, self).save(*args, **kwargs)

class RecomendationDiscription(models.Model):
    imt_min = models.PositiveIntegerField('IMT min')
    imt_max = models.PositiveIntegerField('IMT max')
    title = models.CharField('Title', max_length=50)
    discription = models.TextField('Discription', )

class NutritionComposition(models.Model):
    recomendation_discription_id = models.ForeignKey(RecomendationDiscription, verbose_name='Nutrition composition', on_delete=models.CASCADE,
                                                     related_name='nutrition_composition_recomendation_id')
    title = models.CharField('Title', max_length=50)
    dimension = models.CharField('Dimension', max_length=5,)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['recomendation_discription_id', 'title', 'dimension',], name='unique_nutrition_composition', )
        ]


class NutritionQuide(models.Model):
    elements_id = models.ForeignKey(ElementsQuide, verbose_name='Nutrition',
                                    on_delete=models.CASCADE,related_name='nutrition_quide_recomendation_id')
    estimate = models.PositiveIntegerField('Estimate')
    value = models.DecimalField('Value', max_digits=12, decimal_places=2)
    discription = models.TextField('Discription', )
    man = models.BooleanField('Мужчина?')
    age_min = models.PositiveIntegerField('Age min ')
    age_max = models.PositiveIntegerField('Age max')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['elements_id', 'man', 'age_min',], name='unique_nutrition_quide', )
        ]

class NutritionResult(models.Model):
    recomendation_result_id = models.ForeignKey(RecomendationResult, on_delete=models.CASCADE,
                                                related_name='nutrition_result_recomendation_id')
    elements_id = models.ForeignKey(NutritionQuide, verbose_name='Nutrition',
                                    on_delete=models.CASCADE, related_name='nutrition_result_element_id')



