from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from datetime import datetime, timedelta, timezone, tzinfo, date


# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=50)
    leader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leaderUser', null=True)
    deadline = models.DateField()
    timeFromStart = models.DurationField()
    members = models.ManyToManyField(
        User,
        through='invite',
        through_fields=('team','user'),
        )
    progress = models.IntegerField(default=0, max_length=100)
    #참여도
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    def showMembers(self):
        memList = ["{0}({1})".format(t.profile.userName, t.username) for t in self.members.all()]
        if len(memList) >= 6:
            memList = memList[:5]
            memList += '...'
        return memList
        #return "\n".join("{0}({1})".format(t.profile.userName, t.username) for t in self.members.all())

class Team_todo(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    sequence = models.IntegerField()
    content = models.CharField(max_length=50)
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return self.content


class Invite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    inviter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="invites",
        null=True,
    )

    def __str__(self):
        return "{0} -> {1}".format(self.user, self.team)


class TeamBoard(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    board_type = models.TextField(null=True)
    body = models.TextField()
    writer = models.CharField(max_length=100, default='')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
    views = models.IntegerField(null=True)

    def __str__(self):
        return self.title

class FileTb(models.Model):
    teamboard = models.ForeignKey('teamproject.TeamBoard', on_delete=models.CASCADE, null=True, related_name='teamboards')
    teamFile = models.FileField(upload_to='teamboard/', null=True)
    filename = models.CharField(max_length=100, default='')
        
    def __str__(self):
        return self.filename
        

class CommentTb(models.Model):
    post = models.ForeignKey('teamproject.TeamBoard', on_delete=models.CASCADE, related_name='commentTbs') 
    writer = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    text = models.TextField()
    created_date = models.DateField(default=date.today())
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text