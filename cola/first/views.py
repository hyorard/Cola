from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Board,Comment,profile
from .forms import CommentForm
from django.contrib import auth

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
        # 프로필은 있는데 팀은 없을 때, 마이페이지 들어가면 프로필 또 만들어라고 하는 것 방지
        try:
            TeamList = request.user.team_set.all().values()
            return render(request,'mypage.html', {'Teams':TeamList, 'prof' : prof})
        except:
            return render(request,'mypage.html', {'Teams':None, 'prof' : prof})
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
    boards = Board.objects
    return render(request, 'infoboard.html', {'boards':boards})

def ppt_board(request):
    boards = Board.objects
    return render(request, 'pptboard.html', {'boards':boards})

def presentation_board(request):
    boards = Board.objects
    return render(request, 'presentationboard.html', {'boards':boards})

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
    return render(request, 'detail.html', {'board':board})


def logout(request):
    auth.logout(request)
    return redirect('main')