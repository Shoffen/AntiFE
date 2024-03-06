from django.shortcuts import render, HttpResponse, redirect
from .models import TodoItem, Product, Receptai, Naudotojai
from django.db.models import Q
from django.contrib.auth import authenticate

def home(request):
    return render(request, "home.html")

def todos(request):
    items = TodoItem.objects.all()
    return render(request, "todos.html",  {"todos": items })

def product(request):
    products = Product.objects.all()
    return render(request, 'Product.html', {'products': products})
def receptai_list(request):
    receptai_list = Receptai.objects.all()
    return render(request, 'Receptai.html', {'receptai_list': receptai_list})

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        birthday = request.POST.get('birthday')
        password = request.POST.get('password')
        
        # Save the data to the database
        new_user = Naudotojai(
            el_pastas=email,
            usename=username,
            vardas=name,
            pavarde=surname,
            gimimo_data=birthday,
            password=password,
            level=0  # Set default level or adjust as needed
        )
        new_user.save()
        
        # Redirect to a success page or homepage
        return redirect('/')  # Change 'home' to the name of your homepage URL pattern
        
    return render(request, 'register.html')

from django.contrib.auth import authenticate

def login(request):
    message = None
    if request.method == 'POST':
        username = request.POST.get('surname')
        password = request.POST.get('password')
        user = Naudotojai.objects.filter(usename=username, password=password).first()
        print(user)
        if user is not None:
            # Authentication successful
            message = "Login successful. Welcome, {}".format(username)
            return redirect('/')
            
        else:
            # Authentication failed
            message = "Invalid username or password. Please try again."
            
    return render(request, 'login.html', {'message': message})


