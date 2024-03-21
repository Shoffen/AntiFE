from django.shortcuts import render
from homepage.models import Naudotojai

def profilisview(request):
    user_id = None
    username = None
    vardas = None
    pavarde = None
    telefonas = None
    gimimo_Data = None

    if request.user.is_authenticated:
        user_id = request.user.id
        username = request.user.username
        el_pastas = request.user.email
        try:
            # Assuming there's a OneToOneField or ForeignKey relationship between Naudotojai and User
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
        'vardas' : vardas,
        'pavarde': pavarde,
        'telefonas': telefonas,
        'gimimo_Data': gimimo_Data,
        'el_pastas': el_pastas,
    }
    
    return render(request, 'Profilis.html', context)
