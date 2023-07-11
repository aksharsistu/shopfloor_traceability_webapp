from django.db import models
from stage.models import ListOfStages, CHOICES


class ProductList(models.Model):
    productName = models.CharField(max_length=20, primary_key=True)
    processId = models.CharField(max_length=20)


class ProductData(models.Model):
    productName = models.ForeignKey(ProductList, on_delete=models.CASCADE)
    stageName = models.ForeignKey(ListOfStages, on_delete=models.CASCADE)
    start = models.BooleanField(default=False)
    end = models.BooleanField(default=False)
    qa = models.BooleanField(default=False)
    rework = models.BooleanField(default=False)
    final = models.CharField(max_length=6, choices=CHOICES)
