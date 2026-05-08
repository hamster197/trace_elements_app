from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.db import models
from datetime import date

from apps.elements.models import ElementsQuide
from config.middleware import get_current_user

from apps.products.models import ProductQuide
from apps.questionnaire.constants import GoalChoises


# Create your models here.

class TypeOfActivityQuide(models.Model):
    title = models.CharField('Title', max_length=45, )

    def __str__(self):
        return self.title

class LoadIntensityQuide(models.Model):
    title = models.CharField('Title', max_length=25, unique=True, )
    description = models.CharField('Description', max_length=255, )
    pal = models.DecimalField('pal', max_digits=12, decimal_places=2)

    def __str__(self):
        return self.title


class Questionnaire(models.Model):
    user_id = models.ForeignKey(get_user_model(), verbose_name='User', on_delete=models.CASCADE, related_name='questionnaire_user_id')
    creation_date = models.DateField(default=date.today)
    height = models.PositiveIntegerField(null=False, validators=[MaxValueValidator(2700), ],)
    weight = models.PositiveIntegerField(null=False, validators=[MaxValueValidator(210), ], )
    load_intensity_id = models.ForeignKey(LoadIntensityQuide,verbose_name='Load_intensity',
                                              on_delete=models.CASCADE, related_name='questionnaire_load_intensity_id')
    type_of_activity_id = models.ManyToManyField(TypeOfActivityQuide, verbose_name='Activity type',
                                                 related_name='questionnaire_type_of_activity_id')
    goal_choises = models.CharField('Goal', max_length=65, choices=GoalChoises.choices)
    favorite_foods_id = models.ManyToManyField(ProductQuide, verbose_name='Favorite foods',
                                              related_name='questionnaire_favorite_food_id')
    not_favorite_foods_id = models.ManyToManyField(ProductQuide, verbose_name='Not favorite foods',
                                                  related_name='questionnaire_not_favorite_food_id')

    food_qst = ProductQuide.objects.all()

    class Meta:
        ordering = ['-pk',]
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'creation_date'], name='unique_user_id_creation_date', )
        ]

    def save(self, *args, **kwargs):
        if not self.pk:
            self.user_id = get_current_user()

        return super(Questionnaire, self).save(*args, **kwargs)

    def get_favorite_foods_queruset(self):
        return self.food_qst.exclude(pk__in=self.not_favorite_foods_id.all().values_list('pk'))

    def get_not_favorite_foods_id_queruset(self):
        return self.food_qst.exclude(pk__in=self.favorite_foods_id.all().values_list('pk'))


class QuestionQuide(models.Model):
    text = models.CharField('Question text', max_length=255, unique=True, )
    elements_id = models.ManyToManyField(ElementsQuide, verbose_name='Nutrients attached to the question')

    def __str__(self):
        return self.text

    class Meta:
        ordering =['pk',]

class QuizeResult(models.Model):
    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,  related_name='quize_result_user_id')
    creation_date = models.DateField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'creation_date'], name='unique_user_id_creation_date_quize_result', )
        ]
        ordering =['-creation_date',]

class QuizeResultElement(models.Model):
    quize_id = models.ForeignKey(QuizeResult, on_delete=models.CASCADE, related_name='quize_result_id')
    element_id = models.ForeignKey(ElementsQuide, on_delete=models.CASCADE, related_name='quize_result_elements_id')
    estimation = models.PositiveIntegerField('Estimation', default=0,)
    percent = models.DecimalField('Percent', max_digits=12, decimal_places=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['quize_id', 'element_id'], name='unique_quize_result_element', )
        ]

    def clean(self,):
        self.validate_unique()

    def get_max(self):
        total = QuestionQuide.objects.filter(elements_id=self.element_id).count() * 4

        return total

    def get_status_element(self):
        result = 'No data'
        if self.percent <= 20:
            result = 'low risk/deficiency not detected'
        elif self.percent > 21 and self.percent <= 40:
            result = 'possible mild deficiency'
        elif self.percent > 41 and self.percent <= 70:
            result = 'moderate deficit'
        elif self.percent > 71 and self.percent <= 100:
            result = 'severe deficiency'

        return result

    @classmethod
    def get_today_user_quize_answers(cls):
        return cls.objects.filter(quize_id__user_id=get_current_user(), quize_id__creation_date=date.today())


