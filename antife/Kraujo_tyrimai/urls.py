from django.urls import path
from . import views
from .views import create_kraujo_tyrimas

app_name = 'kraujo_tyrimai'

urlpatterns = [
    path('', views.kraujotyrview, name='kraujotyrview'),
    path('create_kraujo_tyrimas/', create_kraujo_tyrimas, name='create_kraujo_tyrimas'),
]