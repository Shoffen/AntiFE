from django.shortcuts import render

def profilisview(request):
    return render(request, 'Profilis.html')

from django.shortcuts import render

def profilisview(request):
    username = None
    if request.user.is_authenticated:
        user_id = request.user.id
        username = request.user.username
    
    context = {
        'user_id': user_id,
        'username': username  # Include the username in the context
    }
    
    return render(request, 'Profilis.html', context)

