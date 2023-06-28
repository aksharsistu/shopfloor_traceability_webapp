from django.contrib import admin

from barcode.models import Rework, Rejection, Trace

# Register your models here.

admin.site.register(Rework)
admin.site.register(Rejection)
admin.site.register(Trace)
