from django.shortcuts import render, HttpResponse, redirect
from .models import TodoItem, Product, Receptai, Naudotojai
from django.db.models import Q
from django.contrib.auth import authenticate
from django.contrib import messages
from django.http import JsonResponse

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


#dovydo recepto kurimas
def create_recipe_view(request):
    if request.method == 'POST':
        # Extract form data
        recipe_name = request.POST.get('recipeName')
        recipe_summary = request.POST.get('recipeSummary')
        ingredient_names = request.POST.getlist('ingredient[]')
        ingredient_amounts = request.POST.getlist('amount[]')

        # Check if all required fields are present
        if not (recipe_name and recipe_summary):
            return JsonResponse({'error': 'Recipe name and summary are required.'}, status=400)
        
        # Create Recipe object and save to database
        try:
            recipe = Receptai.objects.create(
                pavadinimas=recipe_name,
                aprasas=recipe_summary
            )
            # Check if the recipe was successfully created
            if not recipe:
                return JsonResponse({'error': 'Failed to create recipe.'}, status=500)
            
            # Create ingredient objects for the recipe
            for ingredient, amount in zip(ingredient_names, ingredient_amounts):
                recipe.ingredients.create(name=ingredient, amount=amount)
            
            # Return success response
            return JsonResponse({'message': 'Recipe created successfully!'})
        except Exception as e:
            # Return error response if any exception occurs during creation
            return JsonResponse({'error': str(e)}, status=500)

    # If the request method is not POST, render the template
    products = Product.objects.all()
    return render(request, 'receptukurimas.html', {'products': products})


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






from django.contrib.sessions.models import Session
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

from django.contrib.auth import logout  # Import the logout function

def logout_view(request):
    logout(request)
    return redirect('/')  # Redirect to the homepage or any other desired URL


