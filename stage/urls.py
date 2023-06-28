from django.urls import path

from stage import views

urlpatterns = [
    path('get/', views.get_stage),
    path('set/', views.set_stage),
    path('delete/', views.delete_stage),
    path('stagedata/', views.get_stage_data)
]
