from django.db import models

class GoalChoises(models.TextChoices):
    LoseWeight = 'LoseWeight', 'Lose Weight'
    WeightMaintenance = 'WeightMaintenance', 'Weight Maintenance'
    GainWeight = 'GainWeight', 'Gain Weight'
    ImproveTheQualityOfHealth = 'ImproveTheQualityOfHealth', 'Improve The Quality Of Health'
    Treatment = 'Treatment', 'Treatment'

# answer_choises = (('4', 'Yes'), ('0', 'No'), ('2', 'Sometimes'), )

class QuestionEstimateChoises(models.TextChoices):
    Yes = '4', 'Yes'
    Sometimes = '2', 'Sometimes'
    No = '0', 'No'