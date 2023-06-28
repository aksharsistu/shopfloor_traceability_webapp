from django.contrib import admin

from session.models import UserData, UserLog

# Register your models here.

admin.site.register(UserData)
admin.site.register(UserLog)
