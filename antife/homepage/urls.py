from django.urls import path
from .views import home, todos, product, login, register, receptai_list, logged

urlpatterns = [
   path("", home, name="home"),
   path('todos/', todos, name='todos'),
   path('product/', product, name='product'),
   path('receptai/', receptai_list, name='receptai_list'),
   path('login/', login, name='login'),
   path('register/', register, name='register'),
   path('baseLogged/', logged, name='logged'),
]
