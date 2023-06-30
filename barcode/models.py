from django.db import models
from stage.models import CHOICES
from list.models import Products
from session.models import UserData
from stage.models import StageData


# Create your models here.


class Rejection(models.Model):
    code = models.IntegerField()
    description = models.CharField(max_length=20)


class Rework(models.Model):
    code = models.IntegerField()
    description = models.CharField(max_length=20)


class PermanentTrace(models.Model):
    permanent_sno = models.CharField(max_length=13, null=True)
    sno = models.CharField(max_length=12, primary_key=True)


class Trace(models.Model):
    sno = models.ForeignKey(PermanentTrace, on_delete=models.CASCADE)
    product_name = models.ForeignKey(Products, on_delete=models.CASCADE)
    username = models.ForeignKey(UserData, on_delete=models.CASCADE)
    time = models.DateTimeField()
    stage = models.ForeignKey(StageData, on_delete=models.CASCADE)
    place = models.CharField(max_length=10, choices=CHOICES)
    description = models.CharField(max_length=13)

