from django.db import models

# Create your models here.


class Processes(models.Model):
    process = models.CharField(max_length=20, primary_key=True)
    pid = models.CharField(max_length=50)


class Products(models.Model):
    product_name = models.CharField(max_length=50, primary_key=True)
    process = models.ForeignKey(Processes, on_delete=models.CASCADE, null=True)
    product_code = models.CharField(max_length=5)
    fg_code = models.CharField(max_length=20)
