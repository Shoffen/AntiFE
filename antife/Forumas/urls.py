from django.urls import path
from . import views

app_name = 'Forumas'

urlpatterns = [
    path('', views.forumasview, name='forumasview'),
]
