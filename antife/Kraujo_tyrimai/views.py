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
        
        # Check if both data and fenilalaninas are empty
        if not data and not fenilalaninas:
            messages.error(request, 'Užpildykite formą')
            return redirect('kraujo_tyrimai:kraujotyrview')
        
        # Check if data is empty
        if not data:
            messages.error(request, 'Įveskite datą')
            return redirect('kraujo_tyrimai:kraujotyrview')
        
        # Check if fenilalaninas is empty
        if not fenilalaninas:
            messages.error(request, 'Įveskite fenilalanino kiekį')
            return redirect('kraujo_tyrimai:kraujotyrview')

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




import plotly.express as px
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def kraujotyrview(request):
    # Filter Kraujo_tyrimai instances by the current authenticated user
    kraujo_tyrimai_qs = Kraujo_tyrimai.objects.filter(fk_Naudotojasid_Naudotojas__user=request.user)
    
    if not kraujo_tyrimai_qs:
        # If there are no kraujo tyrimai, render the template without the chart
        return render(request, 'Kraujotyr.html')

    # Extract x (dates) and y (fenilalaninas) data
    lithuanian_month_names = {
        1: 'Sausio',
        2: 'Vasario',
        3: 'Kovo',
        4: 'Balandžio',
        5: 'Gegužės',
        6: 'Birželio',
        7: 'Liepos',
        8: 'Rugpjūčio',
        9: 'Rugsėjo',
        10: 'Spalio',
        11: 'Lapkričio',
        12: 'Gruodžio'
    }
    x = [f"{kraujo_tyrimas.data.strftime('%Y')} {lithuanian_month_names[kraujo_tyrimas.data.month]} {kraujo_tyrimas.data.day}" for kraujo_tyrimas in kraujo_tyrimai_qs]

    y = [kraujo_tyrimas.fenilalaninas for kraujo_tyrimas in kraujo_tyrimai_qs]
    
    # Combine dates and phenylalanine values into tuples
    data_points = list(zip(x, y))
    
    # Sort the data points based on dates
    sorted_data_points = sorted(data_points, key=lambda tup: tup[0])
    
    if not sorted_data_points:
        # If there are no data points, render the template without the chart
        return render(request, 'Kraujotyr.html')

    # Unzip sorted data points into separate lists
    sorted_dates, sorted_phenylalanine = zip(*sorted_data_points)
    
    # Get unique years
    years = sorted(set(date.split(' ')[0] for date in sorted_dates))
    
    # Handle form submission
    if request.method == 'POST':
        selected_year = int(request.POST.get('year'))
        # Filter data points for the selected year
        filtered_data_points = [(date, phenylalanine) for date, phenylalanine in sorted_data_points if date.startswith(str(selected_year))]
        # Unzip filtered data points into separate lists
        sorted_dates, sorted_phenylalanine = zip(*filtered_data_points)
    else:
        # By default, show data points for the most recent year
        selected_year = years[-1]
        # Filter data points for the most recent year
        filtered_data_points = [(date, phenylalanine) for date, phenylalanine in sorted_data_points if date.startswith(str(selected_year))]
        # Unzip filtered data points into separate lists
        sorted_dates, sorted_phenylalanine = zip(*filtered_data_points)
    
    # Create the plot
    fig = px.line(y=sorted_phenylalanine, x=sorted_dates, labels={'x': 'Data', 'y': 'Fenilalaninas µmol/l'},
                  hover_name=sorted_dates)  # Set hover_name to dates
    
    # Add scatter markers with larger size
    fig.add_scatter(x=sorted_dates, y=sorted_phenylalanine, mode='markers', marker=dict(size=10), showlegend=False, hoverinfo='text')

    # Customize hover text and remove legend title
    hover_text = 'Fenilalaninas: %{y}<br>Data: %{x}'
    fig.update_traces(hovertemplate=hover_text)

    
    # Set the default range for the y-axis
    fig.update_layout(yaxis=dict(range=[0, 800]))
    
    # Convert plot to HTML
    chart = fig.to_html()
    
    context = {'chart': chart, 'years': years, 'selected_year': selected_year}
    
    return render(request, 'kraujotyr.html', context)








