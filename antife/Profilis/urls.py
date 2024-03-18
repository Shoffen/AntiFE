from django.urls import path
from . import views

app_name = 'profilis'

urlpatterns = [
    path('', views.profilisview, name='profilisview'),
]