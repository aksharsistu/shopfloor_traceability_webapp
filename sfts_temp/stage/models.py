from django.db import models

CHOICES = (
    ('start', 'start'),
    ('end', 'end'),
    ('qa', 'qa'),
    ('rework', 'rework')
)


class ListOfStages(models.Model):
    stageName = models.CharField(max_length=4, primary_key=True)
    description = models.CharField(max_length=20)


class StageData(models.Model):
    ipAddress = models.GenericIPAddressField(primary_key=True)
    stageName = models.ForeignKey(ListOfStages, on_delete=models.CASCADE)
    placeName = models.CharField(max_length=6, choices=CHOICES)
