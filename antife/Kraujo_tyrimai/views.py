from django.shortcuts import render, redirect
from homepage.models import Kraujo_tyrimai, Naudotojai
from django.contrib.auth.decorators import login_required

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


def kraujotyrview(request):
    return render(request, 'Kraujotyr.html')
