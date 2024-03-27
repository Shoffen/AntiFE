from django.urls import path, include
from . import views

app_name = 'Forumas'

urlpatterns = [
    path('', views.forumasview, name='forumasview'),
    path('create_topic/', views.create_topic, name='create_topic'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]
