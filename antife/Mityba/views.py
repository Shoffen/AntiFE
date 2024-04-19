from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from homepage.models import Product, Receptai, Naudotojai, Valgymai, Valgiarasciai, Recepto_produktai, Naudotojo_receptai, Megstamiausi_receptai, Valgymo_receptas, Valgomas_produktas
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Q, F, Case, Value, When
from django.contrib.auth import authenticate
from django.contrib import messages
from django.http import JsonResponse
from django import forms
from .forms import ValgymasForm
from decimal import Decimal
from django.core.serializers import serialize
import json
import logging, webbrowser
from django.urls import reverse

logger = logging.getLogger(__name__)


def valgiarastis(request):
  naudotojas = Naudotojai.objects.get(user=request.user)
  valgiarasciai = Valgiarasciai.objects.filter(fk_Naudotojasid_Naudotojas=naudotojas)
  valgiarasciai_json = serialize('json', valgiarasciai)
  context = {'valgiarasciai_json': valgiarasciai_json}
  return render(request, 'valgiarastis.html', context)

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
    # Get all recipes
    all_receptai = Receptai.objects.all()
    
    # Get the current user's favorite recipe IDs
    user_favorite_ids = []
    if request.user.is_authenticated:
        current_user = request.user
        naudotojas = Naudotojai.objects.get(user=current_user)
        user_favorite_ids = Megstamiausi_receptai.objects.filter(fk_Naudotojasid_Naudotojas=naudotojas).values_list('fk_Receptasid_Receptas', flat=True)
    
    # Sort recipes based on whether they are in the user's favorites
    sorted_receptai = sorted(all_receptai, key=lambda r: r.id not in user_favorite_ids)
    
    # Render the template with sorted recipes
    return render(request, 'Receptai.html', {'receptai_list': sorted_receptai, 'user_favorite_ids': user_favorite_ids})
    

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
def add_to_favorites(request, recipe_id):
    # Get the current user
    current_user = request.user.naudotojai  # Assuming the user profile is accessible via the 'naudotojai' attribute
    
    # Retrieve the recipe
    recipe = get_object_or_404(Receptai, id=recipe_id)
    
    try:
        # Check if the recipe is already in favorites for the current user
        existing_favorite = Megstamiausi_receptai.objects.filter(fk_Receptasid_Receptas=recipe, fk_Naudotojasid_Naudotojas=current_user)
        if existing_favorite.exists():
            # If the recipe is already in favorites, remove it
            existing_favorite.delete()
            return JsonResponse({'status': 'Recipe removed from favorites'})
        else:
            # If the recipe is not in favorites, add it
            Megstamiausi_receptai.objects.create(fk_Receptasid_Receptas=recipe, fk_Naudotojasid_Naudotojas=current_user)
            return JsonResponse({'status': 'Recipe added to favorites'})
    except Exception as e:
        # Handle any exceptions
        return JsonResponse({'error': str(e)}, status=500)

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
    
def valgymai_open(request):
    selected_date = request.GET.get('selectedDate')
    request.session['selectedDate'] = selected_date
    return valgymai_list(request)

def valgymai_list(request):
    selected_date = request.session.get('selectedDate') 
    naudotojas = Naudotojai.objects.get(user=request.user)

    if selected_date:
        valgymai_list = Valgymai.objects.filter(
            fk_Valgiarastisid_Valgiarastis__data=selected_date,
            fk_Valgiarastisid_Valgiarastis__fk_Naudotojasid_Naudotojas=naudotojas
        ).prefetch_related('valgymo_receptas_set').prefetch_related('valgomas_produktas_set')
    else:
        return render(request, 'valgiarastis.html')
    
    valgymai_list.total_fenilalaninas = 0
    valgymai_list.total_baltymas = 0
    for valgymas in valgymai_list:
        for valgomasreceptas in valgymas.valgymo_receptas_set.all():
            valgomasreceptas.total_fenilalaninas = round(valgomasreceptas.kiekis /100 * Decimal(valgomasreceptas.fk_Receptasid_Receptas.fenilalaninas) , 1)
            valgymai_list.total_fenilalaninas+=valgomasreceptas.total_fenilalaninas
            valgomasreceptas.total_baltymas = round(valgomasreceptas.kiekis /100 * Decimal(valgomasreceptas.fk_Receptasid_Receptas.baltymai) , 1)
            valgymai_list.total_baltymas+=valgomasreceptas.total_baltymas
        for valgomasproduktas in valgymas.valgomas_produktas_set.all():
            valgomasproduktas.total_fenilalaninas = round(valgomasproduktas.kiekis /100 * Decimal(valgomasproduktas.fk_Produktasid_Produktas.phenylalanine) , 1)
            valgymai_list.total_fenilalaninas+=valgomasproduktas.total_fenilalaninas
            valgomasproduktas.total_baltymas = round(valgomasproduktas.kiekis /100 * Decimal(valgomasproduktas.fk_Produktasid_Produktas.protein) , 1)
            valgymai_list.total_baltymas+=valgomasproduktas.total_baltymas

    context = {
        'valgymai_list': valgymai_list,
        'all_receptai': serialize('json', Receptai.objects.all()),
        'all_products': serialize('json', Product.objects.all())
    }
    return render(request, 'valgymas.html', context)

def delete_valgomasReceptas(request, valgymo_receptas_id):
    try:
        valgymo_receptas = Valgymo_receptas.objects.get(id=valgymo_receptas_id)
    except Valgymo_receptas.DoesNotExist:
        return valgymai_list(request)
    if request.method == 'POST':
        valgymo_receptas.delete()
        return valgymai_list(request)
    return valgymai_list(request)
    
def delete_valgomasProduktas(request, valgomas_produktas_id):
    try:
        valgomas_produktas = Valgomas_produktas.objects.get(id=valgomas_produktas_id)
    except Valgomas_produktas.DoesNotExist:
        return valgymai_list(request)
    if request.method == 'POST':
        valgomas_produktas.delete()
        return valgymai_list(request)
    return valgymai_list(request)