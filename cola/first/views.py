from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Board,Comment,profile, BoardFile
from django.contrib import auth
from datetime import date,datetime,timedelta

#pagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def mypage(request):
    if not request.user.is_authenticated:
        return render(request,'login.html')
    try:
        prof = request.user.profile
        TeamList = request.user.team_set.all().values()
        return render(request,'mypage.html', {'Teams':TeamList, 'prof' : prof})
    except:
        return render(request,'profile.html')

def changeProfile(request):
    TeamList = request.user.team_set.all().values()
    return render(request,'profile.html', {'Teams':TeamList})

def makeProfile(request):
    if request.POST['type'] == 'change':
        prof = request.user.profile
    else:
        prof = profile()

    prof.user = request.user

    try:
        prof.img = request.FILES['userPic']
    except:
        pass

    if request.POST['userName'] == '':
        pass
    else:
        prof.userName = request.POST['userName']

    if request.POST['school'] == '':
        pass
    else:
        prof.school = request.POST['school']

    prof.date = date.today()
    prof.save()
    prof = request.user.profile
    TeamList = prof.user.team_set.all().values()
    return render(request,'mypage.html', {'Teams':TeamList, 'prof' : prof})

def board(request):
    boards = Board.objects
    TeamList = request.user.team_set.all().values()
    return render(request, 'board.html', {'boards':boards, 'Teams' : TeamList})

def infoboard(request):
    if not request.user.is_authenticated:
        return render(request,'login.html')
    try:
        prof = request.user.profile
        pass
    except:
        return render(request,'profile.html')
    boards = Board.objects
    boards_list = Board.objects.all()
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
        "Teams" : TeamList,
    }

    return render(request, 'infoboard.html', context)

def searchPost(request):
    searchKey = request.POST['search_key']
    word = request.POST['search']
    
    if searchKey == 'subject':
        boards_list = Board.objects.filter(title__contains=word)
    elif searchKey == 'content':
        boards_list = Board.objects.filter(body__contains=word)
    elif searchKey == 'writer_name':
        boards_list = Board.objects.filter(writer__contains=word)
    
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
      "Teams" : TeamList,
   }

    return render(request, 'infoboard.html', context)
    

    


def detail(request, board_id):
    # 프로필 생성 안했을 시 프로필 생성 페이지로 
    try:
        prof = request.user.profile
        pass
    except:
        # profile X -> makeprofile -> profile.html
        return render(request,'profile.html')
    
    board_detail = get_object_or_404(Board, pk = board_id)
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
    return render(request, 'detail.html', {'board':board_detail, 'check' : check, 'Teams' : TeamList})

def modify(request, board_id):
    board = Board.objects.get(id=board_id)
    
    TeamList = request.user.team_set.all().values()
    return render(request, 'modify.html', {'board':board, 'Teams' : TeamList})

def modifyAction(request, board_id):
    board = get_object_or_404(Board, pk = board_id)
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
                files = BoardFile()
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


def removeBoard(request, board_id):
   
    board = Board.objects.get(id=board_id)
    
    board.delete()
    
    boards = Board.objects
    boards_list = Board.objects.all()
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
        "Teams" : TeamList,
    }
    return render(request, 'infoboard.html', context)

    

def addComment(request):
    boardId = request.POST['boardId']
    post = Board.objects.get(id=boardId)
    comment = Comment()
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
    return render(request, 'detail.html', {'board':post, 'check' : check, 'Teams' : TeamList})

def deleteComment(request):
    boardId = request.POST['boardId']
    post = Board.objects.get(id=boardId)

    commentId = request.POST['commentId']
    comment = Comment.objects.get(id=commentId)
    comment.delete()

    nick = request.user.profile.userName
    # 글쓴이와 들어온 사람이 같은지 확인(삭제/수정)
    
    bw = post.writer
    if bw == nick:
        check = True
    else :
        check = False
    
    TeamList = request.user.team_set.all().values()
    return render(request, 'detail.html', {'board':post, 'check' : check, 'Teams' : TeamList})

def changeComment(request):

    if request.method == "GET":
        boardId = request.GET['boardId']
        post = Board.objects.get(id=boardId)
        commentId = int(request.GET['commentId'])

        nick = request.user.profile.userName
        # 글쓴이와 들어온 사람이 같은지 확인(삭제/수정)
    
        bw = post.writer
        if bw == nick:
            check = True
        else :
            check = False
    
        TeamList = request.user.team_set.all().values()
        return render(request, 'changeComment.html', {'board':post, 'check' : check, 'commentId' : commentId, 'Teams' : TeamList})
    
    else:
        boardId = request.POST['boardId']
        post = Board.objects.get(id=boardId)
        commentId = request.POST['commentId']
        comment = Comment.objects.get(id=commentId)
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
        return render(request, 'detail.html', {'board':post, 'check' : check, 'Teams' : TeamList})



def new(request):
    
    TeamList = request.user.team_set.all().values()
    return render(request, 'new.html', {'Teams' : TeamList})

def create(request):
    board = Board()

    conn_user = request.user
    conn_profile = profile.objects.get(user=conn_user)
    nick = conn_profile.userName
    board.writer = nick
   
    board.title = request.POST['title']
    board.body = request.POST['body'] 
    board.pub_date = timezone.datetime.now()
    board.views = 0
    board.save()
    
    for f in request.FILES.getlist("fileToUpload"):
        #file saving process
        def process(f):
            files = BoardFile()
            files.board = board
            files.boardFile = f
            files.filename = f.name.split('/')[-1]
            files.save()
        process(f)
    
    return redirect('/first/board/'+str(board.id))


def logout(request):
    auth.logout(request)
    return redirect('firstpage')