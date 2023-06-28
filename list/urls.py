from django.urls import path

from list import views

urlpatterns = [
    path('process/get/', views.get_process),
    path('process/set/', views.set_process),
    path('process/delete/', views.delete_process),
    path('product/get/', views.get_product),
    path('product/set/', views.set_product),
    path('product/delete/', views.delete_product)
]
