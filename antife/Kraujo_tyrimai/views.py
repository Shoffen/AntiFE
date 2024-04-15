from django.shortcuts import render, redirect
from homepage.models import Kraujo_tyrimai, Naudotojai
from django.contrib.auth.decorators import login_required
from .utils import get_plot
from django.db.models import Q
from django.contrib import messages



@login_required
def create_kraujo_tyrimas(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        fenilalaninas = request.POST.get('fenilalaninas')
        # Fetch the corresponding Naudotojai instance
        naudotojai_instance = Naudotojai.objects.get(user=request.user)
        # Check if a Kraujotyr already exists for the given date and user
        existing_kraujotyr = Kraujo_tyrimai.objects.filter(Q(data=data) & Q(fk_Naudotojasid_Naudotojas=naudotojai_instance)).exists()
        if existing_kraujotyr:
            # If a Kraujotyr already exists for the given date and user, show an error message
            messages.error(request, 'Kraujo tyrimas su šia data jau egzistuoja.')
        else:
            # If a Kraujotyr for the given date and user doesn't exist, create a new one
            Kraujo_tyrimai.objects.create(data=data, fenilalaninas=fenilalaninas, fk_Naudotojasid_Naudotojas=naudotojai_instance)
            # Add success message
            messages.success(request, 'Kraujo tyrimas sėkmingai pridėtas.')
            # Redirect to the 'kraujotyrview' view after creating the Kraujo Tyrimas
            return redirect('kraujo_tyrimai:kraujotyrview')
    # If the request method is not POST or if there was an error, render the 'kraujotyrview' template
    return kraujotyrview(request)




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








