from django.shortcuts import render, redirect
from homepage.models import Kraujo_tyrimai, Naudotojai
from django.contrib.auth.decorators import login_required
from .utils import get_plot
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
import datetime

@login_required
def create_kraujo_tyrimas(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        fenilalaninas = request.POST.get('fenilalaninas')
        # Fetch the corresponding Naudotojai instance
        naudotojai_instance = Naudotojai.objects.get(user=request.user)
        
        # Validate if the selected date is not exceeded over today's date
        selected_date = datetime.datetime.strptime(data, '%Y-%m-%d').date()
        today = timezone.now().date()
        if selected_date > today:
            # If the selected date is greater than today's date, display an error message
            messages.error(request, 'Pasirinkta negalima data.')
            return redirect('kraujo_tyrimai:kraujotyrview')
        
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
    
    # Extract x (dates) and y (fenilalaninas) data
    x = [kraujo_tyrimas.data for kraujo_tyrimas in kraujo_tyrimai_qs]
    y = [kraujo_tyrimas.fenilalaninas for kraujo_tyrimas in kraujo_tyrimai_qs]
    
    # Combine dates and phenylalanine values into tuples
    data_points = list(zip(x, y))
    
    # Sort the data points based on dates
    sorted_data_points = sorted(data_points, key=lambda tup: tup[0])
    
    # Unzip sorted data points into separate lists
    sorted_dates, sorted_phenylalanine = zip(*sorted_data_points)
    
    # Plot the graph
    chart = get_plot(range(len(sorted_dates)), sorted_phenylalanine, sorted_dates)

    return render(request, 'Kraujotyr.html', {'chart': chart})




