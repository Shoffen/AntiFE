from django.contrib import admin
from .models import TodoItem
from .models import Product
# Register your models here.

admin.site.register(TodoItem)
admin.site.register(Product)