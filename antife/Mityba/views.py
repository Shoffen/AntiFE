from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from homepage.models import Product, Receptai, Naudotojai, Valgymai, Valgiarasciai
from django.db.models import Q, F
from django.contrib.auth import authenticate
from django.contrib import messages
from django.http import JsonResponse
from django import forms
from .forms import ValgymasForm
import json
from homepage.views import get_naudotojas

def valgiarastis(request):
    return render(request, 'valgiarastis.html')

def valgymas(request):
    return render(request, 'valgymas.html')

def product(request):
    query = request.GET.get('query')
    if query:
        products = Product.objects.filter(Q(name__icontains=query))
    else:
        products = Product.objects.all()
    return render(request, 'Product.html', {'products': products})

def receptai_list(request):
    receptai_list = Receptai.objects.all()
    return render(request, 'Receptai.html', {'receptai_list': receptai_list})

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

def create_valgiarastis(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        selected_date = data.get('date_input')
        naudotojas = Naudotojai.objects.get(user=request.user)

        if selected_date:
            existing_valgiarasciai = Valgiarasciai.objects.filter(data=selected_date, fk_Naudotojasid_Naudotojas=naudotojas)
            
            if existing_valgiarasciai.exists():
                return JsonResponse({'status': 'jau yra'})   
            Valgiarastis = Valgiarasciai.objects.create(
                diena=0,
                bendras_fenilalaninas=0,
                data=selected_date,
                fk_Naudotojasid_Naudotojas=naudotojas
            )
            return JsonResponse({'status': 'success'})
    else:
        return render(request, 'valgiarastis.html')

def create_valgymas(request):
    if request.method == 'POST':
        form = ValgymasForm(request.POST)
        if form.is_valid():
            valgymas = form.save(commit=False)
            valgymas.tipas = 'pusryciai'
            valgymas.save()
            return redirect('valgymas_detail', pk=valgymas.pk)
    else:
        form = ValgymasForm()
    return render(request, 'valgymas.html', {'form': form})