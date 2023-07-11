from django.db import models
from process.models import ProcessData
from product.models import ProductData, ProductList
from stage.models import ListOfStages, CHOICES
from user.models import UserData


class Barcode(models.Model):
    barcode = models.CharField(max_length=12)
    description = models.CharField(max_length=13)
    processNo = models.ForeignKey(ProcessData, on_delete=models.CASCADE)
    productName = models.ForeignKey(ProductList, on_delete=models.CASCADE)
    stageName = models.ForeignKey(ListOfStages, on_delete=models.CASCADE)
    placeName = models.CharField(max_length=6, choices=CHOICES)
    username = models.ForeignKey(UserData, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()


class Permanent(models.Model):
    barcode = models.CharField(max_length=12)
    permanent = models.CharField(max_length=13)
