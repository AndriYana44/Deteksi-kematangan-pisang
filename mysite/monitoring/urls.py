from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('grafik/', views.grafik),
    path('upload/', views.upload),
    path('suhu', views.suhu),
    path('suhuapi', views.suhuapi),
]