from django.db import models

class SexChoises(models.TextChoices):
    Man = 'MAN', 'Man'
    Woman = 'WOMAN', 'Woman'
