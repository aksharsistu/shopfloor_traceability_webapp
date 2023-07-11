from django.urls import path
from product import views

urlpatterns = [
    path('get/', views.getProducts),
    path('set/', views.setProduct),
    path('delete/', views.deleteProduct),
]
