from django.db import models

# Create your models here.

CHOICES = (
    ("start", "start"),
    ("end", "end"),
    ("qa", "qa"),
    ("rework", "rework")
)


class StageData(models.Model):
    line_code = models.CharField(max_length=4, primary_key=True)
    line_name = models.CharField(max_length=20)


class Stages(models.Model):
    ip = models.GenericIPAddressField(primary_key=True)
    line_code = models.ForeignKey(StageData, on_delete=models.CASCADE)
    place = models.CharField(max_length=10, choices=CHOICES, default="end")
