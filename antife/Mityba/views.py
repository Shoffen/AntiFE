from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from homepage.models import Product, Receptai, Naudotojai, Valgymai, Valgiarasciai, Recepto_produktai, Naudotojo_receptai
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Q, F
from django.contrib.auth import authenticate
from django.contrib import messages
from django.http import JsonResponse
from django import forms
from .forms import ValgymasForm
from decimal import Decimal
import json


def valgiarastis(request):
    return render(request, 'valgiarastis.html')

def product(request): 
  query = request.GET.get('query')
  category = request.GET.get('category')

  products = Product.objects.all()
  if query:
    products = products.filter(Q(name__icontains=query))
  if category:
    products = products.filter(category=category)
  return render(request, 'Product.html', {'products': products})

def receptai_list(request):
    receptai_list = Receptai.objects.all()
    return render(request, 'Receptai.html', {'receptai_list': receptai_list})

@login_required
def manoreceptai_list(request):
    # Get the current user
    current_user = request.user

    try:
        # Get the Naudotojai instance associated with the current user
        naudotojas = Naudotojai.objects.get(user=current_user)
        # Get all recipe IDs associated with the current user from Naudotojo_Receptai table
        user_recipe_ids = Naudotojo_receptai.objects.filter(fk_Naudotojasid_Naudotojas=naudotojas).values_list('fk_Receptasid_Receptas', flat=True)
        # Fetch the recipes from Receptai model using the retrieved recipe IDs
        receptai_list = Receptai.objects.filter(id__in=user_recipe_ids)
    except Naudotojai.DoesNotExist:
        # If the Naudotojai instance for the current user does not exist, return an empty list of recipes
        receptai_list = []

    return render(request, 'ManoReceptai.html', {'manoreceptai_list': receptai_list})


@login_required
#dovydo recepto kurimas
def create_recipe_view(request):
    if request.method == 'POST':
        # Extract form data
        recipe_name = request.POST.get('recipeName')
        recipe_summary = request.POST.get('recipeSummary')
        ingredient_names = request.POST.getlist('ingredient[]')
        ingredient_amounts = request.POST.getlist('amount[]')

        # Check if all required fields are present
        if not (recipe_name and recipe_summary and ingredient_names and ingredient_amounts):
            return JsonResponse({'error': 'Recipe name, summary, ingredients, and amounts are required.'}, status=400)
        
        try:
            # Create Recipe object and save to database
            recipe = Receptai.objects.create(
                pavadinimas=recipe_name,
                aprasas=recipe_summary,
            )
            
            # Check if the recipe was successfully created
            if not recipe:
                return JsonResponse({'error': 'Failed to create recipe.'}, status=500)
            
            # Associate the user's ID with the created recipe
            naudotojas = Naudotojai.objects.get(user=request.user)
            Naudotojo_receptai.objects.create(fk_Naudotojasid_Naudotojas=naudotojas, fk_Receptasid_Receptas=recipe)
            
            total_phe = 0
            total_calories = 0  # Initialize total calories
            # Create ingredient objects for the recipe
            for ingredient_name, ingredient_amount in zip(ingredient_names, ingredient_amounts):
                # Get or create the product instance
                product, created = Product.objects.get_or_create(name=ingredient_name)
                # Create Recepto_produktai instance
                ingredient_amount_decimal = Decimal(ingredient_amount)
                ingredient_calories = ingredient_amount_decimal * (product.calories / Decimal(100))
                total_calories += ingredient_calories
                ingredient_phe = ingredient_amount_decimal * (product.phenylalanine / Decimal(100))
                total_phe += ingredient_phe
                Recepto_produktai.objects.create(
                    fk_Receptasid_Receptas=recipe,
                    fk_Produktasid_Produktas=product,
                    amount=ingredient_amount_decimal
                )
                
            recipe.kalorijos = total_calories
            recipe.fenilalaninas = total_phe
            recipe.save()
            # Return success response
            return JsonResponse({'message': 'Recipe created successfully!'})
        except Exception as e:
            # Return error response if any exception occurs during creation
            return JsonResponse({'error': str(e)}, status=500)

    # If the request method is not POST, render the template
    products = Product.objects.all()
    return render(request, 'receptukurimas.html', {'products': products})

def remove_recipe_view(request, recipe_id):
    if request.method == 'POST':
        try:
            # Try to get the recipe object from the database
            recipe = Receptai.objects.get(id=recipe_id)
            # Delete the recipe
            recipe.delete()
            return JsonResponse({'success': True})
        except Receptai.DoesNotExist:
            # If recipe with the provided ID does not exist, return an error
            return JsonResponse({'error': 'Recipe not found.'}, status=404)
        except Exception as e:
            # Return error response if any exception occurs during deletion
            return JsonResponse({'error': str(e)}, status=500)
    else:
        # If the request method is not POST, return a bad request error
        return JsonResponse({'error': 'Bad request.'}, status=400)

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
            tipai = ["Pusryčiai", "Pietūs", "Vakarienė", "Papildomi"]
            for tipas in tipai:
                Valgymai.objects.create(
                    tipas=tipas,
                    fk_Valgiarastisid_Valgiarastis=Valgiarastis
                )
            return JsonResponse({'status': 'success'})
    else:
        return render(request, 'valgiarastis.html')

def valgymai_list(request):
    selected_date = request.GET.get('selectedDate')
    naudotojas = Naudotojai.objects.get(user=request.user)
    print("Selected date:", selected_date)

    if selected_date:
        valgymai_list = Valgymai.objects.filter(
            fk_Valgiarastisid_Valgiarastis__data=selected_date,
            fk_Valgiarastisid_Valgiarastis__fk_Naudotojasid_Naudotojas=naudotojas
        ).prefetch_related('valgymo_receptas_set').prefetch_related('valgomas_produktas_set')
    else:
        return render(request, 'valgiarastis.html')
    
    valgymai_list.total_fenilalaninas = 0
    for valgymas in valgymai_list:
        for valgomasreceptas in valgymas.valgymo_receptas_set.all():
            valgomasreceptas.total_fenilalaninas = round(valgomasreceptas.kiekis /100 * Decimal(valgomasreceptas.fk_Receptasid_Receptas.fenilalaninas) , 1)
            valgymai_list.total_fenilalaninas+=valgomasreceptas.total_fenilalaninas
        for valgomasproduktas in valgymas.valgomas_produktas_set.all():
            valgomasproduktas.total_fenilalaninas = round(valgomasproduktas.kiekis /100 * Decimal(valgomasproduktas.fk_Produktasid_Produktas.phenylalanine) , 1)
            valgymai_list.total_fenilalaninas+=valgomasproduktas.total_fenilalaninas


    context = {'valgymai_list': valgymai_list}
    return render(request, 'valgymas.html', context)