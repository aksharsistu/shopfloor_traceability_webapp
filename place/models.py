from django.db import models

from list.models import Processes
from stage.models import CHOICES, StageData


# Create your models here.


class PlaceData(models.Model):
    process = models.ForeignKey(Processes, on_delete=models.CASCADE)
    stage = models.OneToOneField(StageData, on_delete=models.CASCADE)
    start = models.BooleanField(default=False)
    end = models.BooleanField(default=False)
    qa = models.BooleanField(default=False)
    rework = models.BooleanField(default=False)
    final = models.CharField(max_length=10, choices=CHOICES)
