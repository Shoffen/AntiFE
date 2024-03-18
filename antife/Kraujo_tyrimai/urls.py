from django.urls import path
from . import views

app_name = 'kraujo_tyrimai'

urlpatterns = [
    path('', views.kraujotyrview, name='kraujotyrview'),
]