from django.urls import path

from barcode import views

urlpatterns = [
    path('', views.index),
    path('generate/', views.generate)
]
