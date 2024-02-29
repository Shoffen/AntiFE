from django.urls import path
from . import views

urlpatterns = [
    
   path("", views.home, name="home" ),
   path('todos/', views.todos, name='Todos'),
<<<<<<< Updated upstream
   path('login/', views.login, name = 'login'),
   path('register/', views.register, name = 'register')
]
=======
   path('login/', views.login, name ='Login'),
   path('register/', views.register, name = 'Register'),
  
   
]
>>>>>>> Stashed changes
