from django.shortcuts import render, HttpResponse, redirect
from .models import TodoItem, Product, Receptai, Naudotojai
from django.db.models import Q
from django.contrib.auth import authenticate
from django.contrib import messages

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
def logged(request):
    return render(request, "baseLogged.html")

from django.shortcuts import render, redirect
from .models import Naudotojai

from django.shortcuts import render, redirect
from .models import Naudotojai
import re

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Naudotojai
import re

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        name = request.POST.get('name')
        lastName = request.POST.get('lastName')
        phoneNumber = request.POST.get('phoneNumber')
        birthday = request.POST.get('birthday')
        password = request.POST.get('password')
        
        # Validate email format using regular expression
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messages.error(request, 'Neteisingas elektronio pašto formatas')
        elif Naudotojai.objects.filter(el_pastas=email).exists():
            # Set the message if the email already exists
            messages.error(request, 'Šis paštas jau naudojamas')
        else:
            # Save the data to the database
            new_user = Naudotojai(
                el_pastas=email,
                usename=username,
                vardas=name,
                telefonas=phoneNumber,
                pavarde=lastName,
                gimimo_data=birthday,
                password=password,
                level=0  # Set default level or adjust as needed
            )
            new_user.save()
            messages.success(request, 'Registracija sėkminga! Galite prisijungti')
            return redirect('/')  # Change 'home' to the name of your homepage URL pattern
    
    return render(request, 'register.html')







from django.contrib import messages

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = Naudotojai.objects.filter(usename=username, password=password).first()
        if user is not None:
            # Authentication successful
            messages.success(request, f"Sėkmingai prisijungėte. Sveiki, {username}")
            return render(request, 'baseLogged.html')  # Redirect to another URL with success message
        else:
            # Authentication failed
            messages.error(request, "Neteisingi prisijungimo duomenys. Bandykite dar kart.")

    return render(request, 'login.html')





