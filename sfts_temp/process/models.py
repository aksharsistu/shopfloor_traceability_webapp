from django.db import models
from product.models import ProductData, ProductList
from stage.models import ListOfStages


class ProcessData(models.Model):
    processNo = models.IntegerField(primary_key=True)
    productName = models.ForeignKey(ProductList, on_delete=models.CASCADE)
    startingSNo = models.CharField(max_length=12)
    endingSNo = models.CharField(max_length=12)
    maxQuantity = models.IntegerField()
    currentQuantity = models.IntegerField()


class Quantity(models.Model):
    processNo = models.ForeignKey(ProcessData, on_delete=models.CASCADE)
    productName = models.ForeignKey(ProductList, on_delete=models.CASCADE)
    stageName = models.ForeignKey(ListOfStages, on_delete=models.CASCADE)
    quantity = models.IntegerField()
