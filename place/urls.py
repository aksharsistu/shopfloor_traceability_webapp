from django.urls import path

from place import views

urlpatterns = [
    path('get/', views.get_place),
    path('set/', views.set_place)
]
