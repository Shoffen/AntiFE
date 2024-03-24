from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from homepage.models import Forumai, Irasai, Naudotojai
from datetime import date

def forumasview(request):
    # Fetch existing topics with their posted date
    topics = Forumai.objects.all().prefetch_related('irasai_set')  # Prefetch related posts for efficiency
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    return render(request, 'Forumas.html', {'topics': topics, 'username': username})

def create_topic(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        text = request.POST.get('text')
        user = request.user  # Get the current logged-in user
        today = date.today()
        # Create a new topic
        forum = Forumai.objects.create(pavadinimas=title)
        # Create a new post (Irasai) under this topic
        Irasai.objects.create(tekstas=text, data=today, fk_Forumasid_Forumas=forum, fk_Naudotojasid_Naudotojas=user.naudotojai)
        return redirect('Forumas:forumasview')
    else:
        # Handle GET request if necessary
        pass