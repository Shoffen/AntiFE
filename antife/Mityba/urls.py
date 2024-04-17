from django.urls import path
from . import views

app_name = 'Mityba'

urlpatterns = [
    # Define your URL patterns here
    path('product/', views.product, name='product'),
    path('receptai_list/', views.receptai_list, name='receptai_list'),
    path('create_recipe/', views.create_recipe_view, name='create_recipe'),
    path('valgiarastis/', views.valgiarastis, name='valgiarastis'),
    path('create_valgiarastis/', views.create_valgiarastis, name='create_valgiarastis'),
    path('receptai_list/<int:recipe_id>/', views.remove_recipe_view, name='remove_recipe'),
    path('valgymai/', views.valgymai_list, name='valgymai_list'),
]