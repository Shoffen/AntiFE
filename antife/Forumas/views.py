from django.shortcuts import render

def forumasview(request):
    return render(request, 'Forumas.html')
