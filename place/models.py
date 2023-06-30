from django.db import models

from stage.models import Stages, CHOICES


# Create your models here.


class PlaceData(models.Model):
    stage = models.OneToOneField(Stages, on_delete=models.CASCADE)
    start = models.BooleanField(default=False)
    end = models.BooleanField(default=False)
    qa = models.BooleanField(default=False)
    rework = models.BooleanField(default=False)
    final = models.CharField(max_length=10, choices=CHOICES)
