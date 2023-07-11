from django.urls import path
from barcode import views

urlpatterns = [
    path('log/', views.log),
    path('check/', views.check)
]
