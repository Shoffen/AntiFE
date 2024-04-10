from django.shortcuts import render, redirect
from homepage.models import Kraujo_tyrimai, Naudotojai
from django.contrib.auth.decorators import login_required
from .utils import get_plot

@login_required
def create_kraujo_tyrimas(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        fenilalaninas = request.POST.get('fenilalaninas')
        # Fetch the corresponding Naudotojai instance
        naudotojai_instance = Naudotojai.objects.get(user=request.user)
        # Create Kraujo Tyrimas for the current authenticated user
        Kraujo_tyrimai.objects.create(data=data, fenilalaninas=fenilalaninas, fk_Naudotojasid_Naudotojas=naudotojai_instance)
        return render(request, 'Kraujotyr.html')  # Redirect to some success page
    return render(request, 'kraujo_tyrymai.html')


import matplotlib.pyplot as plt

def kraujotyrview(request):
    # Filter Kraujo_tyrimai instances by the current authenticated user
    kraujo_tyrimai_qs = Kraujo_tyrimai.objects.filter(fk_Naudotojasid_Naudotojas__user=request.user)
    
    # Extract unique dates and sort them
    unique_dates = sorted(set(kraujo_tyrimai_qs.values_list('data', flat=True)))

    # Extract x and y values only for the current user's Kraujo_tyrimai instances
    x = [kraujo_tyrimas.data for kraujo_tyrimas in kraujo_tyrimai_qs]
    y = [kraujo_tyrimas.fenilalaninas for kraujo_tyrimas in kraujo_tyrimai_qs]

    # Sort the data based on x values
    sorted_indices = sorted(range(len(x)), key=lambda k: x[k])
    x_sorted = [x[i] for i in sorted_indices]
    y_sorted = [y[i] for i in sorted_indices]

    # Plot the graph
    chart = get_plot(x_sorted, y_sorted)

    # Set x-axis ticks to only include unique dates
    plt.xticks(unique_dates, rotation=45, ha='right')

    return render(request, 'Kraujotyr.html', {'chart': chart})








