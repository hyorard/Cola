from django.contrib import auth, messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Team,Invite,Team_todo, TeamBoard, CommentTb, FileTb
from first.models import profile
from datetime import date,datetime,timedelta
from math import floor
from django.contrib.auth.models import User
#pagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime

from django.contrib import messages
# Create your views here.


def createTeam(request):
    if not request.user.is_authenticated:
        return render(request,'login.html')
    if request.method == 'GET':

        try:
            prof = request.user.profile
            pass
        except:
            # profile X -> makeprofile -> profile.html
            return render(request,'profile.html')
        TeamList = request.user.team_set.all().values()
        return render(request, 'createTeam.html',{'Teams':TeamList})
    
    # team info, create team
    elif request.method == 'POST':
        '''create team'''
        t1 = Team()
        t1.name = request.POST['teamName']
        t1.leader = request.user

        # deadline
        strDeadline = request.POST['deadline']
        dateDeadline = datetime.strptime(strDeadline, "%Y-%m-%d").date()
        t1.deadline = dateDeadline

        # timeFromStart
        intTime = int(request.POST['fromStart'])
        print(intTime)
        t1.timeFromStart = timedelta(intTime)

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
    try:
        prof = request.user.profile
        pass
    except:
        # profile X -> makeprofile -> profile.html
        return render(request,'profile.html')
    # 유저가 속한 모든 팀 리스트
    TeamList = request.user.team_set.all().values()
    try:
        TeamList[0]
    # 팀이 하나도 없을 때,
    except IndexError:
        return render(request, 'createTeam.html')

    if request.method == 'POST':
        teamId = request.POST['teamId']
        team = Team.objects.get(id=teamId)
        members = team.showMembers()
        progressList = team.team_todo_set.all().values()

        updateProgress(team)
        TeamList = request.user.team_set.all().values()
        return render(request, 'teamInfo.html', {'team':team, 'members':members, 'progressList':progressList,'Teams':TeamList})
    else:
        print("############################teaminfo")
        return render(request,'teampage.html')

def updateDeadline(team):
    dt_deadline = datetime.combine(team.deadline, datetime.min.time())
    team.timeFromStart = dt_deadline - datetime.now()
        
    team.deadline = team.deadline.strftime('%Y년%m월%d일'.encode('unicode-escape').decode()).encode().decode('unicode-escape')

def updateProgress(team):
    todos = list(team.team_todo_set.all())
    rate = 0
    for progress in todos:
        if progress.is_finished:
            rate += 1
    try:
        rate /= len(todos)
    except:
        rate = 0

    team.progress = floor(rate*100)
    team.save()
    updateDeadline(team)

def createTodo(request):
    teamId = request.POST['teamId']
    team = Team.objects.get(id=teamId)

    toDo = Team_todo()
    toDo.team = team
    members = team.showMembers()
    toDo.content = request.POST['content']
    try:
        seq = list(team.team_todo_set.all())[-1].sequence
    except:
        seq = 0
    toDo.sequence = seq + 1
    toDo.save()

    updateProgress(team)
    progressList = team.team_todo_set.all().values()
    TeamList = request.user.team_set.all().values()
    return render(request, 'teamInfo.html', {'team':team, 'members':members, 'progressList':progressList,'Teams':TeamList})

def deleteTodo(request):
    teamId = request.POST['teamId']
    team = Team.objects.get(id=teamId)
    todos = list(team.team_todo_set.all())

    for todo in todos:
        try:
            if request.POST[str(todo.sequence)] == 'on':
                todo.delete()
        except:
            pass
    
    updateProgress(team)
    members = team.showMembers()
    progressList = team.team_todo_set.all().values()
    TeamList = request.user.team_set.all().values()
    return render(request, 'teamInfo.html', {'team':team, 'members':members, 'progressList':progressList,'Teams':TeamList})

def changeTodo(request):
    teamId = request.POST['teamId']
    team = Team.objects.get(id=teamId)
    todos = list(team.team_todo_set.all())

    for todo in todos:
        try:
            if request.POST[str(todo.sequence)] != '':
                todo.content = request.POST[str(todo.sequence)]
                todo.save()
        except:
            pass
    
    members = team.showMembers()
    progressList = team.team_todo_set.all().values()
    updateProgress(team)
    TeamList = request.user.team_set.all().values()
    return render(request, 'teamInfo.html', {'team':team, 'members':members, 'progressList':progressList,'Teams':TeamList})

def finishTodo(request):
    teamId = request.POST['teamId']
    team = Team.objects.get(id=teamId)
    todos = list(team.team_todo_set.all())


    for todo in todos:
        try:
            if request.POST[str(todo.sequence)] == 'finished':
                todo.is_finished = True
                todo.save()
            elif request.POST[str(todo.sequence)] == 'unfinished':
                todo.is_finished = False
                todo.save()
        except:
            pass
    
    updateProgress(team)
    members = team.showMembers()
    progressList = team.team_todo_set.all().values()
    TeamList = request.user.team_set.all().values()
    return render(request, 'teamInfo.html', {'team':team, 'members':members, 'progressList':progressList,'Teams':TeamList})

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
        TeamList = request.user.team_set.all().values()
        return render(request, 'changeTeamInfo.html', {'team':team,'Teams':TeamList})
    # 팀 정보 변경 창에서 정보 입력하고 변경시
    # try -> 정보 입력시 변경
    # except -> 정보 미입력시 패스
    except:
        teamId = request.POST['teamId']
        team = Team.objects.get(id=teamId)

        if request.POST['teamName'] == '':
            pass
        else:
            team.name = request.POST['teamName']

        # 리더 변경 ? : team.leader
        # 팀원 추방 ? : team.members ( manytomany )

        try:
            strDeadline = request.POST['deadline']
            dateDeadline = datetime.strptime(strDeadline, "%Y-%m-%d").date()
            team.deadline = dateDeadline
        except:
            pass

        try:
            team.progress = int(request.POST['progress'])
        except:
            pass

        try:
            if request.POST['is_finished'] == 'finished':
                team.is_finished = True
            else:
                team.is_finished = False
        except:
            pass
        
        team.save()
        
        teamId = request.POST['teamId']
        team = Team.objects.get(id=teamId)
        members = team.showMembers()
        progressList = team.team_todo_set.all().values()
        dt_deadline = datetime.combine(team.deadline, datetime.min.time())
        team.timeFromStart = dt_deadline - datetime.now()
        
        team.deadline = team.deadline.strftime('%Y년%m월%d일'.encode('unicode-escape').decode()).encode().decode('unicode-escape')
        TeamList = request.user.team_set.all().values()
        return render(request, 'teamInfo.html', {'team':team, 'members':members, 'progressList':progressList,'Teams':TeamList})

        
def searchPerson(request,team_id=None):
    # 초대하는 팀
    scoutingTeamId = team_id
    scoutingTeam = Team.objects.get(id=team_id)

    


    # teamInfo창에서 팀원추가 버튼 누름
    if request.method == 'GET':
        return render(request,'searchPerson.html', {'scoutingTeam':scoutingTeam})

    # 검색 창에서 초대할 팀원 아이디 검색
    else:
        # 초대할 멤버
        newMemberId = request.POST['newMemberId']
        try:
            newMember = User.objects.get(username=newMemberId)
        except: # 없으면 없다고 알림
            return render(request, 'searchPerson.html', {'error' : '찾는 이메일이 없습니다.', 'scoutingTeam':scoutingTeam})
        
        # 프로필 안 만든 사람이면 거른다
        try:
            newMember.profile.userName
        except:
            return render(request, 'searchPerson.html', {'error' : '프로필을 만들지 않은 사용자입니다.', 'scoutingTeam':scoutingTeam})
        
        # 이미 초대가 된 멤버라면 teamInfo로
        try:
            Invite.objects.get(user=newMember, team=scoutingTeam)
            members = scoutingTeam.showMembers()
            progressList = scoutingTeam.team_todo_set.all().values()
            TeamList = request.user.team_set.all().values()
            return render(request, 'teamInfo.html', {'team':scoutingTeam, 'members':members, 'progressList':progressList,'Teams':TeamList})
        except:
            pass
        # 초대 받은 적이 없다면 초대
        scout = Invite(
                    user = newMember,
                    team = scoutingTeam,
                    inviter = request.user,
                )
        scout.save()

        # 초대했다고 알림
        messages.info(request, '{0}가 {1}를 {2}에 초대하였습니다.'.format(
            request.user.profile.userName,
            newMember.profile.userName,
            scoutingTeam.name))
        # 초대 후 멤버 리스트 업데이트
        members = scoutingTeam.showMembers()
        progressList = scoutingTeam.team_todo_set.all().values()
        TeamList = request.user.team_set.all().values()
        return render(request, 'teamInfo.html', {'team':scoutingTeam, 'members':members, 'progressList':progressList,'Teams':TeamList})


def teamBoard(request, team_id):
    team = Team.objects.get(id=team_id)

    teamboards = team.teamboard_set.all()
    paginator = Paginator(teamboards, 10)
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    
    TeamList = request.user.team_set.all().values()
    context = {
      "object_list" : queryset,
      "team" : team,
      "Teams" : TeamList
   }
    
    return render(request, 'teamBoard.html', context)
def teamboard_new(request, team_id):
    team = Team.objects.get(id=team_id)
    time = datetime.today()
    TeamList = request.user.team_set.all().values()
    return render(request, 'teamnew.html', {'team' : team, 'time' : time,'Teams':TeamList})

def teamboard_write(request, team_id=None):
    if request.method == "POST":    
        teamId = request.POST['teamId']
        team = Team.objects.get(id=teamId)

        board=TeamBoard()
        
        board.team = team
        board.title = request.POST['title']
        board.body = request.POST['body']
        board.views = 0

        conn_user = request.user
        conn_profile = profile.objects.get(user=conn_user)
        nick = conn_profile.userName
        board.writer = nick
        board.pub_date = datetime.now()
        board.save()
        # 글쓴이와 들어온 사람이 같은지 확인(삭제/수정)
        
        for f in request.FILES.getlist("fileToUpload"):
            #file saving process
            def process(f):
                files = FileTb()
                files.teamboard = board
                files.teamFile = f
                files.filename = f.name.split('/')[-1]
                files.save()
            process(f)
        
        teamboards = team.teamboard_set.all()

        bw = board.writer
        if bw == nick:
            check = True
        else :
            check = False
        TeamList = request.user.team_set.all().values()
        return render(request, 'teamdetail.html', {'board':board, 'check' : check,'Teams':TeamList})

def teamdetail(request, board_id):
    board_detail = get_object_or_404(TeamBoard, pk = board_id)
    board_detail.views += 1
    board_detail.save()
    
    conn_user = request.user
    conn_profile = profile.objects.get(user=conn_user)
    nick = conn_profile.userName
    # 글쓴이와 들어온 사람이 같은지 확인(삭제/수정)
    
    bw = board_detail.writer
    if bw == nick:
        check = True
    else :
        check = False
    TeamList = request.user.team_set.all().values()
    return render(request, 'teamdetail.html', {'board':board_detail, 'check' : check, 'Teams':TeamList})

def removeBoardTb(request, board_id):
    board = get_object_or_404(TeamBoard, pk = board_id)
    board.delete()

    boards = TeamBoard.objects
    boards_list = TeamBoard.objects.all()
    paginator = Paginator(boards_list, 10)
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    TeamList = request.user.team_set.all().values()
    context = {
      "object_list" : queryset,
      "Teams":TeamList
   }

    return render(request, 'teamBoard.html', context)

def modifyTb(request, board_id):
    board = TeamBoard.objects.get(id=board_id)
    
    TeamList = request.user.team_set.all().values()
    return render(request, 'teammodify.html', {'board':board, 'Teams' : TeamList})

def modifyActionTb(request, board_id):
    board = get_object_or_404(TeamBoard, pk = board_id)
    if request.POST['title'] == '' and request.POST['body'] == '':
        pass
    elif request.POST['title'] == '':
        board.body = request.POST['body']
    
    elif request.POST['body'] == '':
        board.title = request.POST['title']
    else:
        board.title = request.POST['title']
        board.body = request.POST['body']
        board.pub_date = timezone.datetime.now()
    board.save()
    if request.POST['filechange']:
        #원래 올린 파일 삭제
        bs = board.boards.all()
        for was in bs:
            if was.filename:
                was.delete()
        #새로운 파일로 첨부파일 수정        
        for f in request.FILES.getlist("fileToUpload"):
            #file saving process
            def process(f):
                files = FileTb()
                files.board = board
                files.boardFile = f
                files.filename = f.name.split('/')[-1]
                files.save()
            process(f)
    
    conn_user = request.user
    conn_profile = profile.objects.get(user=conn_user)
    nick = conn_profile.userName
    # 글쓴이와 들어온 사람이 같은지 확인(삭제/수정)
    
    bw = board.writer
    if bw == nick:
        check = True
    else :
        check = False

    TeamList = request.user.team_set.all().values()
    return render(request, 'detail.html', {'board':board, 'check' : check, 'Teams' : TeamList}) 

def addCommentTb(request):
    boardId = request.POST['boardId']
    post = TeamBoard.objects.get(id=boardId)
    comment = CommentTb()
    comment.post = post
    comment.writer = request.user
    comment.text = request.POST['content']
    comment.save()

    nick = request.user.profile.userName
    # 글쓴이와 들어온 사람이 같은지 확인(삭제/수정)
    
    bw = post.writer
    if bw == nick:
        check = True
    else :
        check = False
    TeamList = request.user.team_set.all().values()
    return render(request, 'teamdetail.html', {'board':post, 'check' : check, 'Teams':TeamList})

def deleteCommentTb(request):
    boardId = request.POST['boardId']
    post = TeamBoard.objects.get(id=boardId)

    commentId = request.POST['commentId']
    comment = CommentTb.objects.get(id=commentId)
    comment.delete()

    nick = request.user.profile.userName
    # 글쓴이와 들어온 사람이 같은지 확인(삭제/수정)
    
    bw = post.writer
    if bw == nick:
        check = True
    else :
        check = False
    TeamList = request.user.team_set.all().values()
    return render(request, 'teamdetail.html', {'board':post, 'check' : check, 'Teams':TeamList})

def changeCommentTb(request):

    if request.method == "GET":
        boardId = request.GET['boardId']
        post = TeamBoard.objects.get(id=boardId)
        commentId = int(request.GET['commentId'])

        nick = request.user.profile.userName
        # 글쓴이와 들어온 사람이 같은지 확인(삭제/수정)
    
        bw = post.writer
        if bw == nick:
            check = True
        else :
            check = False
        TeamList = request.user.team_set.all().values()
        return render(request, 'changeCommentTb.html', {'board':post, 'check' : check, 'commentId' : commentId,'Teams':TeamList})
    
    else:
        boardId = request.POST['boardId']
        post = TeamBoard.objects.get(id=boardId)
        commentId = request.POST['commentId']
        comment = CommentTb.objects.get(id=commentId)
        comment.text = request.POST['content']
        comment.save()

        nick = request.user.profile.userName
        # 글쓴이와 들어온 사람이 같은지 확인(삭제/수정)
    
        bw = post.writer
        if bw == nick:
            check = True
        else :
            check = False
        TeamList = request.user.team_set.all().values()
        return render(request, 'teamdetail.html', {'board':post, 'check' : check,'Teams':TeamList})
