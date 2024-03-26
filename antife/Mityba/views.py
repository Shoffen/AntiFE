from django.shortcuts import render, HttpResponse, redirect
from homepage.models import Product, Receptai, Naudotojai, Valgymai, Valgiarasciai, Recepto_produktai
from django.db.models import Q, F, Sum, ExpressionWrapper, DecimalField
from django.contrib.auth import authenticate
from django.contrib import messages
from django.http import JsonResponse
from django import forms
from .forms import ValgymasForm
from decimal import Decimal

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
                print(total_calories)
                print(ingredient_amount)
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
        selected_date = request.POST.get('date-input')
        if selected_date:
            Valgiarasciai = Valgiarasciai.objects.create(
                diena=0,
                fenilalaninas=0,
                data=selected_date,
                naudotojas=1
            )
            return redirect('success_url')
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