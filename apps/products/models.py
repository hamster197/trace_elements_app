from django.db import models

# Create your models here.
class FoodStructure(models.Model):
    title = models.CharField('Title', max_length=45, blank=False,  unique=True,)
    value = models.DecimalField('Value', max_digits=12, decimal_places=2)
    unit_of_measurement = models.CharField('Measurement unit', max_length=15, blank=False, )

    def clean(self,):
        self.validate_unique()

    def __str__(self):
        return self.title

    class Meta:
        abstract = True

class CaloriesQuide(FoodStructure):
    pass


class ChemicalCompositionQuide(FoodStructure):
    pass

class ProductQuide(models.Model):
    title = models.CharField('Title', max_length=45, unique=True,)
    image = models.ImageField('Image', upload_to='media/products')
    calories = models.ManyToManyField(CaloriesQuide, verbose_name='Calories', )
    chemical_composition = models.ManyToManyField(ChemicalCompositionQuide, verbose_name='Chemical composition', )

    def __str__(self):
        return self.title