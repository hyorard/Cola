from django.db import models

# Create your models here.
class Board(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    body = models.TextField()

    def __str__(self):
        return self.title

class profile(models.Model):
    userId = models.models.CharField(max_length=50)
    img = models.ImageField(upload_to='images/')
    school = models.CharField(max_length=50)
    date = models.DateField(auto_now=False, auto_now_add=False)

