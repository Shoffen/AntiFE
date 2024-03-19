from django.shortcuts import render, HttpResponse, redirect
from homepage.models import Product, Receptai, Naudotojai
from django.db.models import Q
from django.contrib.auth import authenticate
from django.contrib import messages
from django.http import JsonResponse

def valgiarastis(request):
    return render(request, 'valgiarastis.html')

def product(request):
    query = request.GET.get('query')
    if query:
        products = Product.objects.filter(name__icontains=query)
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
