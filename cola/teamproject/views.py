from django.contrib import auth
from django.shortcuts import render,redirect
from .models import Team,Invite
import datetime

# Create your views here.

def teamproject(request):
    if not request.user.is_authenticated:
        return render(request,'login.html')
    return render(request, 'teamproject.html')

def createTeam(request):
    if request.method == 'GET':
        return render(request, 'createTeam.html')

    # team info, create team
    elif request.method == 'POST':
        '''create team'''
        t1 = Team()
        t1.name = request.POST['teamName']
        t1.leader = request.user

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
            user = t1.leader,
            team = t1,
            inviter = request.user,
            )
        creation.save()

        return redirect('mypage')

def teamInfo(request):
    if not request.user.is_authenticated:
        return render(request,'login.html')
    if request.method == 'POST':
        teamId = request.POST['teamId']
        team = Team.objects.get(id=teamId)
        members = team.showMembers()
        return render(request, 'teamInfo.html', {'team':team, 'members':members})

'''
변경할 때 몇 개 안 적어놓고 변경하면 오류 뜸 디버깅 ㄱㄱ
'''
def changeTeamInfo(request):
    try:
        request.POST['type']
        teamId = request.POST['teamId']
        team = Team.objects.get(id=teamId)
        return render(request, 'changeTeamInfo.html', {'team':team})
    except:
        teamId = request.POST['teamId']
        team = Team.objects.get(id=teamId)
        team.name = request.POST['teamName']
        # 리더 변경 ? : team.leader
        # 팀원 추방 ? : team.members ( manytomany )

        strDeadline = request.POST['deadline']
        dateDeadline = datetime.datetime.strptime(strDeadline, "%Y-%m-%d").date()
        team.deadline = dateDeadline

        team.progress = request.POST['progress']
        if request.POST['is_finished'] == 'finished':
            team.is_finished = True
        else:
            team.is_finished = False
        team.save()
        members = team.showMembers()
        return render(request, 'teamInfo.html', {'team':team, 'members':members})

