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
지난 시간 -> 남은 시간으로 구현 변경 ㄱㄱ
지난 시간 기능도 안하고 있음
'''
def changeTeamInfo(request):
    # 팀 정보 창에서 변경 요청 시
    try:
        request.POST['type']
        teamId = request.POST['teamId']
        team = Team.objects.get(id=teamId)
        return render(request, 'changeTeamInfo.html', {'team':team})
    # 팀 정보 변경 창에서 정보 입력하고 변경시
    # try -> 정보 입력했으면 변경
    # except -> 정보 미입력했으면 pass
    except:
        teamId = request.POST['teamId']
        team = Team.objects.get(id=teamId)

        try:
            team.name = request.POST['teamName']
        except:
            pass

        # 리더 변경 ? : team.leader
        # 팀원 추방 ? : team.members ( manytomany )

        try:
            strDeadline = request.POST['deadline']
            dateDeadline = datetime.datetime.strptime(strDeadline, "%Y-%m-%d").date()
            team.deadline = dateDeadline
        except:
            pass

        try:
            team.progress = request.POST['progress']
        except:
            pass

        try:
            if request.POST['is_finished'] == 'finished':
                team.is_finished = True
            else:
                team.is_finished = False
        except:
            pass

        try:
            team.save()
        except:
            pass
        
        teamId = request.POST['teamId']
        team = Team.objects.get(id=teamId)
        members = team.showMembers()
        return render(request, 'teamInfo.html', {'team':team, 'members':members})

