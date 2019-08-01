from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Board,Comment,profile
from .forms import CommentForm
from django.contrib import auth

#pagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def main(request):
    # not logged in -> main.html
    if not request.user.is_authenticated:
        return render(request, 'main.html')
    # logged in
    userId = request.user.username
    try:
        # profile O -> main.html
        prof = request.user.profile
        return render(request, 'main.html')
    except:
        # profile X -> makeprofile -> profile.html
        return render(request,'profile.html')

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
    return render(request,'profile.html')

def makeProfile(request):
    if request.POST['type'] == 'change':
        prof = request.user.profile
    else:
        prof = profile()
    prof.user = request.user
    prof.img = request.FILES['userPic']
    prof.userName = request.POST['userName']
    prof.school = request.POST['school']
    prof.date = timezone.datetime.now()
    prof.save()
    return redirect('main')

def board(request):
    boards = Board.objects
    return render(request, 'board.html', {'boards':boards})

def infoboard(request):
    if not request.user.is_authenticated:
        return render(request,'login.html')
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
    context = {
		"object_list" : queryset,
	}

    return render(request, 'infoboard.html', context)

def detail(request, board_id):
    board_detail = get_object_or_404(Board, pk = board_id)
    conn_user = request.user
    conn_profile = profile.objects.get(user=conn_user)
    nick = conn_profile.userName
    # 글쓴이와 들어온 사람이 같은지 확인(삭제/수정)
    
    bw = board_detail.writer
    if bw == nick:
        check = True
    else :
        check = False
    return render(request, 'detail.html', {'board':board_detail, 'check' : check})

def modify(request, board_id):
    board = get_object_or_404(Board, pk = board_id)
    return render(request, 'modify.html', {'board':board})

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

    conn_user = request.user
    conn_profile = profile.objects.get(user=conn_user)
    nick = conn_profile.userName
    # 글쓴이와 들어온 사람이 같은지 확인(삭제/수정)
    
    bw = board.writer
    if bw == nick:
        check = True
    else :
        check = False
    return render(request, 'detail.html', {'board':board, 'check' : check}) 


def removeBoard(request, board_id):
    board = get_object_or_404(Board, pk = board_id)
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
    context = {
		"object_list" : queryset,
	}

    return render(request, 'infoboard.html', context)



def add_comment_to_post(request, board_id):
    post = get_object_or_404(Board, pk=board_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return render(request, 'detail.html', {'board':post})
    else:
        form = CommentForm()
    return render(request, 'add_comment_to_post.html', {'form': form})

def new(request):
    return render(request, 'new.html')

def create(request):
    board = Board()
    conn_user = request.user
    conn_profile = profile.objects.get(user=conn_user)
    nick = conn_profile.userName
    board.writer = nick
    board.title = request.GET['title']
    board.body = request.GET['body']
    board.pub_date = timezone.datetime.now()
    board.save()
    return redirect('/first/board/'+str(board.id))


def logout(request):
    auth.logout(request)
    return redirect('main')