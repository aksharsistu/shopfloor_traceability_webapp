from django.db import models

# Create your models here.

CHOICES = (
    ("start", "start"),
    ("end", "end")
)


class StageData(models.Model):
    line_code = models.CharField(max_length=4, primary_key=True)
    line_name = models.CharField(max_length=20)


class Stages(models.Model):
    ip = models.GenericIPAddressField(primary_key=True)
    line_code = models.ForeignKey(StageData, on_delete=models.CASCADE)
    stage = models.CharField(max_length=5, choices=CHOICES, default="end")
