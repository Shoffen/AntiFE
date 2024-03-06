from django.shortcuts import render, HttpResponse
from .models import TodoItem, Product, Receptai


def home(request):
    return render(request, "home.html")

def todos(request):
    items = TodoItem.objects.all()
    return render(request, "todos.html",  {"todos": items })

def product(request):
    products = Product.objects.all()
    return render(request, 'Product.html', {'products': products})

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def receptai_list(request):
    receptai_list = Receptai.objects.all()
    return render(request, 'Receptai.html', {'receptai_list': receptai_list})
