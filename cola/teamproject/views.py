from django.contrib import auth
from django.shortcuts import render



# Create your views here.

def teamproject(request):
    if not request.user.is_authenticated:
        return render(request,'login.html')
    return render(request,'teamproject.html')