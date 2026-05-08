from django.db import models
from apps.elements.constants import SexChoises

# Create your models here.
class ElementsQuide(models.Model):
    title = models.CharField('Tilte', max_length=30, blank=False, )
    min_value = models.DecimalField('Min value', max_digits=12, decimal_places=2)
    max_value = models.DecimalField('Max value', max_digits=12, decimal_places=2)
    sex = models.CharField('Sex', max_length=30, choices=SexChoises.choices, blank=True, )
    unit = models.CharField('Unit', max_length=30, blank=True)

    class Meta:
        ordering = ['pk',]
        constraints = [
            models.UniqueConstraint(fields=['title', 'sex'], name='unique_title_sex_element_quide', )
        ]

    def __str__(self):
        return  f"{self.title} - {self.get_sex_display()}"

