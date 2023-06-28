from django.db import models


# Create your models here.


class UserData(models.Model):
    username = models.CharField(max_length=10, primary_key=True)
    password = models.CharField(max_length=10)
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    employee_id = models.CharField(max_length=10)
    superuser = models.BooleanField(default=False)


class UserLog(models.Model):
    username = models.ForeignKey(UserData, on_delete=models.CASCADE)
    login_time = models.DateTimeField(null=True)
    logout_time = models.DateTimeField(null=True)
