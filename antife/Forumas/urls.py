from django.urls import path
from . import views

app_name = 'Forumas'

urlpatterns = [
    path('', views.forumasview, name='forumasview'),
    path('create_topic/', views.create_topic, name='create_topic'),
]
