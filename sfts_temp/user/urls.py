from django.urls import path

from user import views

urlpatterns = [
    path('login/', views.login),
    path('register/', views.register),
    path('delete/', views.delete)
]
