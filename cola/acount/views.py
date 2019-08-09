from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages

# Create your views here.
def signup(request):
    if request.method == 'POST':
        try:
            if request.POST['password1'] == request.POST['password2']:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                return redirect('login')
        except:
            messages.warning(request, '다시 회원가입 해주세요')
            #return render(request,'signup.html')
    return render(request, 'signup.html')


# 콜라 로그인 용
def login(request):
    if request.method == 'POST':
        username = request.POST['id']
        password = request.POST['pass']
        user = auth.authenticate(request, username=username, password=password)
        if user:
            auth.login(request, user)
            return redirect('firstpage')
        else:
            return render(request, 'login.html')

    return render(request, 'login.html')


def firstpage(request, teamList=None):
    return render(request, 'firstpage.html')
