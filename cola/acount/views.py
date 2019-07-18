from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth


# Create your views here.
def signup(request):
    if request.method == 'POST':
        try:
            if request.POST['pass1'] == request.POST['pass2']:
                user = User.objects.create_user(request.POST['id'], password=request.POST['pass1'])
                return redirect('login')
        except:
            return render(request,'signup.html')
    return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['id']
        password = request.POST['pass']
        user = auth.authenticate(request, username=username, password=password)

        if user:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'fuck'})

    return render(request, 'login.html')

def home(request):
    return render(request, 'home.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('login')
    return render(request, 'login')