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
            messages.error(request, 'Invalid email format. Please enter a valid email address.')
        elif Naudotojai.objects.filter(el_pastas=email).exists():
            # Set the message if the email already exists
            messages.error(request, 'Email is already registered.')
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
            messages.success(request, 'Registration successful. Now you can login!')
            return redirect('/login')  # Change 'home' to the name of your homepage URL pattern
    
    return render(request, 'register.html')






from django.contrib.sessions.models import Session
from django.contrib import messages

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = Naudotojai.objects.filter(usename=username, password=password).first()
        if user is not None:
            # Authentication successful
            messages.success(request, f"Login successful. Welcome, {username}")
            return redirect('/')  # Redirect to another URL with success message
        else:
            # Authentication failed
            messages.error(request, "Invalid username or password. Please try again.")

    return render(request, 'login.html')

from django.contrib.auth import logout  # Import the logout function

def logout_view(request):
    logout(request)
    return redirect('/')  # Redirect to the homepage or any other desired URL


