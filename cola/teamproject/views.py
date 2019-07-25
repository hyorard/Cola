from django.contrib import auth
from django.shortcuts import render,redirect
from .models import Team,Invite
import datetime

# Create your views here.

def teamproject(request):
    if not request.user.is_authenticated:
        return render(request,'login.html')
    return render(request, 'teamproject.html')

def teamPage(request):
    if not request.user.is_authenticated:
        return render(request,'login.html')
    return render(request, 'teampage.html')

def createTeam(request):
    if request.method == 'GET':
        return render(request, 'createTeam.html')

    # team info, create team
    elif request.method == 'POST':
        '''create team'''
        t1 = Team()
        t1.name = request.POST['teamName']

        # deadline
        strDeadline = request.POST['deadline']
        dateDeadline = datetime.datetime.strptime(strDeadline, "%Y-%m-%d").date()
        t1.deadline = dateDeadline

        # timeFromStart
        intTime = int(request.POST['fromStart'])
        t1.timeFromStart = datetime.timedelta(intTime)

        t1.progress = request.POST['progress']
        t1.save()

        '''invite creator'''
        creation = Invite(
            user = request.user,
            team = t1,
            inviter = request.user,
            )
        creation.save()

        return redirect('mypage')