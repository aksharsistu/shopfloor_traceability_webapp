from django.db import models


class UserData(models.Model):
    username = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=20)
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    employeeId = models.CharField(max_length=10)
    superuser = models.BooleanField(default=False)
