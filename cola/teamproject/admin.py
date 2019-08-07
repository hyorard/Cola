from django.contrib import admin
from .models import Team,Invite,Team_todo, TeamBoard, CommentTb 


# Register your models here.
admin.site.register(Team)
admin.site.register(Invite)
admin.site.register(Team_todo)
admin.site.register(TeamBoard)
admin.site.register(CommentTb)