from django.db import models
from datetime import datetime, timedelta, timezone, tzinfo, date

# Create your models here.
class Board(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    body = models.TextField()

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey('first.Board', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=date.today())
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

class profile(models.Model):
    userId = models.CharField(max_length=50,default= '')
    userName = models.CharField(max_length=10,default='')
    img = models.ImageField(upload_to='images/')
    school = models.CharField(max_length=50)
    date = models.DateField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.userName


