from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Board,Comment,profile
from .forms import CommentForm
from django.contrib import auth

# Create your views here.
def main(request):
    print("entered main########")
    return render(request, 'main.html')

# username : parameter passed by func 'login'
def mypage(request, username=None):
    userId = username
    try:
        # profile had been already made
        prof = profile.objects.get(userId__exact=userId)
        return render(request, 'main.html')
    except:
        # no profile
        return redirect('makeProfile', {'profile':None,'userId':userId})

def makeProfile(request, username=None):
    if request.method == 'GET':
        userId = request.GET['userId']
        return render(request, 'profile.html', {'profile':1, 'userId':userId})
    else:
        if request.POST['type'] == 'change':
            userId = request.POST['userId']
            prof = profile.objects.get(userId__exact=userId)
        else:
            prof = profile()
        prof.img = request.POST.get('userPic','')
        prof.userId = request.POST['userId']
        prof.userName = request.POST['userName']
        prof.school = request.POST['school']
        prof.date = timezone.datetime.now()
        prof.save()
        return redirect('mypage', prof.userId)

def board(request):
    boards = Board.objects
    return render(request, 'board.html', {'boards':boards})

def detail(request, board_id):
    board_detail = get_object_or_404(Board, pk = board_id)
    return render(request, 'detail.html', {'board':board_detail})

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
    board.title = request.GET['title']
    board.body = request.GET['body']
    board.pub_date = timezone.datetime.now()
    board.save()
    return redirect('/board/'+str(board.id))


def logout(request):
    print("fucking logout")
    auth.logout(request)
    print("fucking logout2222222222")
    return redirect('main')