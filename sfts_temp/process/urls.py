from django.urls import path

from process import views

urlpatterns = [
    path('set/', views.setProcess),
    path('get/', views.getProcess),
    path('delete/', views.deleteProcess),
    path('number/', views.generateNumbers),
    path('quantity/', views.getStageQuantity)
]
