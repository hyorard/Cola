from django.contrib import admin
from .models import Team,Invite,Team_todo


# Register your models here.
admin.site.register(Team)
admin.site.register(Invite)
admin.site.register(Team_todo)