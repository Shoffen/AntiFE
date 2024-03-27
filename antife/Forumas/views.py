from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from homepage.models import Forumai, Irasai, Naudotojai
from datetime import date
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def forumasview(request):
    # Fetch existing topics with their posted date
    topics = Forumai.objects.all().prefetch_related('irasai_set')  # Prefetch related posts for efficiency
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    return render(request, 'Forumas.html', {'topics': topics, 'username': username})

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
