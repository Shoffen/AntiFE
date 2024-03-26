from django.shortcuts import render
from homepage.models import Naudotojai

def profilisview(request):
    user_id = None
    username = None
    vardas = None
    pavarde = None
    telefonas = None
    gimimo_Data = None
    el_pastas = None
    password = None

    if request.user.is_authenticated:
        user_id = request.user.id
        username = request.user.username
        el_pastas = request.user.email
        password = request.user.password
        try:
            # Retrieve the latest data from the database
            naudotojas = Naudotojai.objects.get(user=request.user)
            vardas = naudotojas.vardas
            pavarde = naudotojas.pavarde
            telefonas = naudotojas.telefonas
            gimimo_Data = naudotojas.gimimo_data
        except Naudotojai.DoesNotExist:
            # Handle the case where there's no related Naudotojai instance for the current user
            pass

    context = {
        'user_id': user_id,
        'username': username,
        'password': password,
        'vardas': vardas,
        'pavarde': pavarde,
        'telefonas': telefonas,
        'gimimo_Data': gimimo_Data,
        'el_pastas': el_pastas,
    }
    
    return render(request, 'Profilis.html', context)



from django.utils.dateparse import parse_date
from django.shortcuts import redirect
from homepage.models import Naudotojai

def save_profile_changes(request):
    if request.method == 'POST':
        # Retrieve form data from the request
        username = request.POST.get('username')
        vardas = request.POST.get('vardas')
        pavarde = request.POST.get('pavarde')
        telefonas = request.POST.get('telefonas')
        gimimo_data = request.POST.get('birthday')  # Get the date string from the form

        # Parse the date string into a Python date object
        

        el_pastas = request.POST.get('el_pastas')

        # Retrieve the user's profile from the database
        naudotojas = Naudotojai.objects.get(user=request.user)

        # Update the user's email
        if el_pastas:
            request.user.email = el_pastas
            request.user.save()

       
        naudotojas.gimimo_data = gimimo_data

        # Update the profile fields
        if vardas:
            naudotojas.vardas = vardas
        if pavarde:
            naudotojas.pavarde = pavarde
        if telefonas:
            naudotojas.telefonas = telefonas
        if el_pastas:
            naudotojas.el_pastas = el_pastas

        # Save the updated profile
        naudotojas.save()

        # Redirect the user to the profile page or any other page as needed
        return redirect('profilis:profilisview')






