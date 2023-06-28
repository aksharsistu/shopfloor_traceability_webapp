from django.urls import path

from session import views

urlpatterns = [
    path('login/', views.login),
    path('logout/', views.logout),
    path('register/', views.register),
    path('delete/', views.delete)
]
