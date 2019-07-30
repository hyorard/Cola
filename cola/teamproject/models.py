from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render,redirect

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
    #자료조사파일
    refFile = models.FileField(default = 0, upload_to='refFile/', null=True)
    ################
    #product = models.FileField(upload_to=) ppt
    #참여도
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    def showMembers(self):
        return "\n".join("{0}({1})".format(t.profile.userName, t.username) for t in self.members.all())



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
