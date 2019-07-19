from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Board,profile

# Create your views here.
def main(request):
    return render(request, 'main.html')

def board(request):
    boards = Board.objects
    return render(request, 'board.html', {'boards':boards})

def detail(request, board_id):
    board_detail = get_object_or_404(Board, pk = board_id)
    return render(request, 'detail.html', {'board':board_detail})

def new(request):
    return render(request, 'new.html')

def create(request):
    board = Board()
    board.title = request.GET['title']
    board.body = request.GET['body']
    board.pub_date = timezone.datetime.now()
    board.save()
    return redirect('/board/'+str(board.id))

def mypage(request):
    return render(request, 'mypage.html')

def profile(request):
    prf = profile.objects
    return render(request, 'mypage.html', {'profile':prf})