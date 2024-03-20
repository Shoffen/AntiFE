from django.shortcuts import render, HttpResponse, redirect
from .models import Naudotojai
from django.db.models import Q
from django.contrib.auth import authenticate
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.sessions.models import Session
import re

def home(request):
    return render(request, "home.html")

def loged(request):
    return render(request, "baseLogged.html")

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User


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
            # Hash the password
            hashed_password = make_password(password)
            
            # Save the data to the database
            new_user = Naudotojai(
                el_pastas=email,
                username=username,
                vardas=name,
                telefonas=phoneNumber,
                pavarde=lastName,
                gimimo_data=birthday,
                password=hashed_password,  # Save hashed password
                level=0  # Set default level or adjust as needed
            ) 
            new_user.save() 
            user = User.objects.create_user(username, email, password)
            user.save()
            messages.success(request, 'Registration successful. Now you can login!')
            return redirect('/login')  # Change 'home' to the name of your homepage URL pattern
    
    return render(request, 'register.html')



from django.contrib.auth import authenticate, login as django_login
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Naudotojai

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
            
        if user is not None and user.is_active:
            django_login(request, user)
            messages.success(request, f"Login successful. Welcome, {username}")
            return render(request, 'base.html')  # Redirect to the base logged page
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    
    return render(request, 'login.html')





from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    request.session.flush()  # Clear all session data
    return redirect('/')  # Redirect to the homepage or any other desired URL


