from django.urls import path
from stage import views

urlpatterns = [
    path('set/', views.setStage),
    path('get/', views.getStage),
    path('delete/', views.deleteStage),
    path('list/', views.listStage)
]
