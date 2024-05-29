from django.shortcuts import render, redirect
from homepage.models import Kraujo_tyrimai, Naudotojai
from django.contrib.auth.decorators import login_required
from .utils import get_plot
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
import datetime
from datetime import datetime
import plotly.express as px

@login_required
def create_kraujo_tyrimas(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        fenilalaninas = request.POST.get('fenilalaninas')
        selected_year = request.POST.get('selected_year')  # Retrieve selected year

        print(selected_year)
      # Check if selected_year is 'None' as a string
        
        if not data or not fenilalaninas:
            messages.error(request, 'Užpildykite formą')
            return redirect('kraujo_tyrimai:kraujotyrview', selected_year)  # Pass selected year
        
        # Fetch the corresponding Naudotojai instance
        naudotojai_instance = Naudotojai.objects.get(user=request.user)
        
        data_obj = datetime.strptime(data, '%Y-%m-%d').date()
        today = datetime.now().date()
        
        if data_obj > today:
            # If the selected date is greater than today's date, display an error message
            messages.error(request, 'Pasirinkta negalima data.')
            return redirect('kraujo_tyrimai:kraujotyrview', selected_year)  # Pass selected year
        
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
        
        # Redirect to the 'kraujotyrview' view with the selected year
        return redirect('kraujo_tyrimai:kraujotyrview', selected_year)

    # If the request method is not POST, render the 'kraujotyrview' template
    return redirect('kraujo_tyrimai:kraujotyrview', selected_year)

from django.shortcuts import render, redirect
from django.http import JsonResponse



    
def deleteTyrimas(request):

    selected_data = request.POST.get('selectedDataPointId')
    selected_year = int(request.POST.get('selected_year'))  # Retrieve selected year
    print("OOOOOOOOOOOOOOOOOOOOO"+selected_data)
    clicked_date = getData(selected_data)
    
    kraujotyrimas_obj = Kraujo_tyrimai.objects.filter(data=clicked_date)
        
    kraujotyrimas_obj.delete()
    messages.success(request, 'Kraujo tyrimas sėkmingai pašalintas.')
    return redirect('kraujo_tyrimai:kraujotyrview', selected_year=selected_year)

def getData(selected_data):
        # Split the date string by spaces and take the first element as the year
        clicked_year = selected_data.split(' ')[0].strip()
        print(clicked_year)

        # Split the date string by spaces and take the third element as the month name
        clicked_month_lithuanian = selected_data.split(' ')[2].strip()
        print(clicked_month_lithuanian)

        clicked_day = selected_data.split(' ')[3].strip()
        print(clicked_day)  # Output: 7

        # Map Lithuanian month names to English
        lithuanian_to_english_month = {
            'Sausio': '01',
            'Vasario': '02',
            'Kovo': '03',
            'Balandžio': '04',
            'Gegužės': '05',
            'Birželio': '06',
            'Liepos': '07',
            'Rugpjūčio': '08',
            'Rugsėjo': '09',
            'Spalio': '10',
            'Lapkričio': '11',
            'Gruodžio': '12',
        }

        # Convert Lithuanian month name to numeric representation
        clicked_month = lithuanian_to_english_month.get(clicked_month_lithuanian, '01')  # Default to January if not found
        print('Clicked Month:', clicked_month)

            # Parse the selected date
        clicked_date = datetime(int(clicked_year), int(clicked_month), int(clicked_day)).date()
        return clicked_date


@login_required
def saveTyrimas(request):
    if request.method == 'POST':
        # Retrieve the edited data and selected data point ID from the request
        edited_date = request.POST.get('editedDate')
        edited_fenilalaninas = request.POST.get('editedFenilalaninas')
        print("NUUUUUUUUUUUUUUUUUUUUUU" + edited_date)
        print("NUUUUUUUUUUUUUUUUUUUUUU" + edited_fenilalaninas)
        selected_data = request.POST.get('selectedDataPointId')
        #selected_data_point_id = request.POST.get('selectedDataPointId')
        selected_year = int(request.POST.get('selected_year'))  # Retrieve selected year

        
        clicked_date = getData(selected_data)
        print(clicked_date)
        kraujotyrimas_obj = Kraujo_tyrimai.objects.get(data=clicked_date)
        
        data_obj = datetime.strptime(edited_date, '%Y-%m-%d').date()
        today = datetime.now().date()
        print(clicked_date)
        print(edited_date)
         # Ensure edited_date is a datetime.date object
        edited_date = datetime.strptime(edited_date, '%Y-%m-%d').date()

        if data_obj > today:
            # If the selected date is greater than today's date, display an error message
            messages.error(request, 'Pasirinkta negalima data.')
            return redirect('kraujo_tyrimai:kraujotyrview', selected_year=selected_year)  # Pass selected year
        # Fetch the corresponding Naudotojai instance
        
        if clicked_date!=edited_date:
            naudotojai_instance = Naudotojai.objects.get(user=request.user)
            existing_kraujotyr = Kraujo_tyrimai.objects.filter(Q(data=edited_date) & Q(fk_Naudotojasid_Naudotojas=naudotojai_instance)).exists()
            if existing_kraujotyr:
                # If a Kraujotyr already exists for the given date and user, show an error message
                messages.error(request, 'Kraujo tyrimas su šia data jau egzistuoja.')
            else:
                kraujotyrimas_obj.data = edited_date
                kraujotyrimas_obj.fenilalaninas =edited_fenilalaninas
                kraujotyrimas_obj.save()
                messages.success(request, 'Kraujo tyrimas sėkmingai atnaujintas.')
        else:
                kraujotyrimas_obj.data = edited_date
                kraujotyrimas_obj.fenilalaninas =edited_fenilalaninas
                kraujotyrimas_obj.save()
                messages.success(request, 'Kraujo tyrimas sėkmingai atnaujintas.')

    
        
        

    return redirect('kraujo_tyrimai:kraujotyrview', selected_year=selected_year)  # Pass selected year








            
@login_required
def kraujotyrview(request, selected_year=None):
    # Filter Kraujo_tyrimai instances by the current authenticated user
    kraujo_tyrimai_qs = Kraujo_tyrimai.objects.filter(fk_Naudotojasid_Naudotojas__user=request.user)
    
    if not kraujo_tyrimai_qs:
        # If there are no kraujo tyrimai, render the template without the chart
        return render(request, 'Kraujotyr.html', {'years': [], 'selected_year': None, 'chart': None})

    # Extract x (dates) and y (fenilalaninas) data
    x = [kraujo_tyrimas.data for kraujo_tyrimas in kraujo_tyrimai_qs]
    y = [kraujo_tyrimas.fenilalaninas for kraujo_tyrimas in kraujo_tyrimai_qs]
    
    # Combine dates and phenylalanine values into tuples
    data_points = list(zip(x, y))
    
    # Sort the data points based on dates
    sorted_data_points = sorted(data_points, key=lambda tup: tup[0])
    
    if not sorted_data_points:
        # If there are no data points, render the template without the chart
        return render(request, 'Kraujotyr.html', {'years': [], 'selected_year': None, 'chart': None})

    # Extract sorted dates and phenylalanine
    sorted_dates, sorted_phenylalanine = zip(*sorted_data_points)
    
    # Get unique years
    years = sorted(set(date.year for date in sorted_dates))
    
    # Initialize selected_year outside the conditional block
    if selected_year is None:
        selected_year = years[-1]  # By default, show data points for the most recent year
    
    # Handle form submission
    if request.method == 'POST':
        selected_year = int(request.POST.get('year'))
    
    # Filter data points for the selected year
    filtered_data_points = [(date, phenylalanine) for date, phenylalanine in sorted_data_points if date.year == selected_year]
    
    # Unzip filtered data points into separate lists
    if filtered_data_points:
        sorted_dates, sorted_phenylalanine = zip(*filtered_data_points)
    else:
        sorted_dates, sorted_phenylalanine = [], []
    
    # Define color thresholds
    green_zone = (120, 600)
    orange_threshold = 800  # Adjust as needed
    
    # Assign colors to data points based on proximity to thresholds
    colors = []
    for phenylalanine in sorted_phenylalanine:
        if phenylalanine >= green_zone[0] and phenylalanine <= green_zone[1]:
            colors.append('green')  # Green zone
        elif phenylalanine > orange_threshold:
            colors.append('red')  # Far from good zone
        else:
            colors.append('orange')  # Close to good zone
    
    # Convert sorted dates to formatted Lithuanian month names
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
    formatted_dates = [f"{date.strftime('%Y')} - {lithuanian_month_names[date.month]} {date.day}" for date in sorted_dates]
    
    # Create the plot if there is data
    if sorted_phenylalanine and formatted_dates:
        fig = px.line(
            x=formatted_dates,
            y=sorted_phenylalanine,
            labels={'x': 'Data', 'y': 'Fenilalaninas µmol/l'},
            title='Fenilalaninas per metus'
        )
        fig.add_scatter(x=formatted_dates, y=sorted_phenylalanine, mode='markers', marker=dict(size=10, color=colors), name="", hoverinfo='none')

        # Customize hover text
        hover_text = 'Fenilalaninas: %{y}<br>Data: %{x}'
        fig.update_traces(hovertemplate=hover_text)

        # Determine the maximum value of Fenilalaninas
        max_fenilalaninas = max(sorted_phenylalanine, default=0)
        
        # Set the default range for the y-axis to be at least 800
        y_axis_upper_limit = max(800, max_fenilalaninas * 1.1)  # Ensure at least 800
        
        fig.update_layout(yaxis=dict(range=[0, y_axis_upper_limit]))
        # Update layout to disable legend
        fig.update_layout(showlegend=False)

        num_points = len(filtered_data_points)
        print(num_points)
        if num_points > 1:
            # Define the green background zone, always including it regardless of the number of points
            fig.update_layout(
        shapes=[
            # Green rectangle for the background
            {
                'type': 'rect',
                'x0': formatted_dates[0] if formatted_dates else "",  # Start date of the green zone
                'x1': formatted_dates[-1] if formatted_dates else "",  # End date of the green zone
                'y0': green_zone[0],  # Lower limit of the y-axis
                'y1': green_zone[1],  # Upper limit of the y-axis
                'fillcolor': 'rgba(173, 255, 47, 0.2)',  # Green color with opacity
                'line': {'width': 0},  # No border line
                'layer': 'below',  # Ensure the green zone is below the main plot
            },
        ]
    )
        else:
           
            # Define the green background zone
            fig.update_layout(
    shapes=[
        # Green rectangle for the background
        {
            'type': 'rect',
            'x0': 0,  # Start date of the green zone (assuming it starts at the beginning of the x-axis)
            'x1': 1,  # End date of the green zone (assuming it extends to the end of the x-axis)
            'y0': 120,  # Lower limit of the y-axis for the green zone
            'y1': 600,  # Upper limit of the y-axis for the green zone
            'fillcolor': 'rgba(173, 255, 47, 0.2)',  # Green color with opacity
            'line': {'width': 0},  # No border line
            'layer': 'below',  # Ensure the green zone is below the main plot
        },
    ]
)

        
        
        # Convert plot to HTML
        chart = fig.to_html()
    else:
        chart = "<p>Neliko tyrimų susijusių su pasirinktais metais</p>"
    
    # Ensure context is always defined
    context = {'chart': chart, 'years': years, 'selected_year': selected_year}
    
    return render(request, 'kraujotyr.html', context)
