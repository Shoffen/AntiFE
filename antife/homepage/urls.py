from django.urls import path
from .views import home, todos, product, login, register

urlpatterns = [
   path("", home, name="home"),
   path('todos/', todos, name='todos'),
   path('product/', product, name='product'),
   path('login/', login, name='login'),
   path('register/', register, name='register'),
]
