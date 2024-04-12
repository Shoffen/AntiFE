from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from homepage.models import Forumai, Irasai, Naudotojai, Komentarai
from datetime import date
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

@login_required
def add_comment(request, irasas_id):
    if request.method == 'POST':
        text = request.POST.get('text')
        try:
            irasas = Irasai.objects.get(id=irasas_id)
        except ObjectDoesNotExist:
            return render(request, 'error_page.html', {'error_message': 'Irasai does not exist'}, status=404)

        if hasattr(request.user, 'naudotojai'):
            naudotojas = request.user.naudotojai
        else:
            return render(request, 'error_page.html', {'error_message': 'User does not have related naudotojai'}, status=400)

        Komentarai.objects.create(tekstas=text, fk_Irasasid_Irasas=irasas, fk_Naudotojasid_Naudotojas=naudotojas, data=date.today())
        return redirect(reverse('Forumas:forumasview'))  # Redirect to the forum home page
    else:
        # Handle GET requests if needed
        return HttpResponse("Only POST requests are allowed", status=405)

@login_required
def forumasview(request):
    topics = Forumai.objects.all().prefetch_related('irasai_set')
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    irasai_list = []
    for topic in topics:
        irasai_list.append((topic, topic.irasai_set.all()))
    return render(request, 'Forumas.html', {'topics': irasai_list, 'username': username})

@login_required
def create_topic(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        text = request.POST.get('text')
        if title and text:  # Check if both title and text are provided
            user = request.user
            today = date.today()
            forum = Forumai.objects.create(pavadinimas=title)
            Irasai.objects.create(tekstas=text, data=today, fk_Forumasid_Forumas=forum, fk_Naudotojasid_Naudotojas=user.naudotojai)
            messages.success(request, 'Topic created successfully.')
            return redirect('Forumas:forumasview')
        else:
            messages.error(request, 'Please provide both title and text.')
            return redirect('Forumas:forumasview')  # Redirect back to the forum view
    return render(request, 'Forumas.html', {})  # Render the forum page for GET requests
