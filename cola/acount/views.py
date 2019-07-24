from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth


# Create your views here.
def signup(request):
    if request.method == 'POST':
        try:
            if request.POST['password1'] == request.POST['password2']:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                return redirect('login')
        except:
            return render(request,'signup.html')
    return render(request, 'signup.html')


# 콜라 로그인 용
def login(request):
    if request.method == 'POST':
        username = request.POST['id']
        password = request.POST['pass']
        user = auth.authenticate(request, username=username, password=password)

        if user:
            auth.login(request, user)
            return redirect('main')
        else:
            return render(request, 'login.html')

    return render(request, 'login.html')



# 소셜 로그인 용
def social(request):
    return render(request, 'Profile.html')

def firstpage(request):
    return render(request, 'firstpage.html')
'''
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('login')
    return render(request, 'login')
'''