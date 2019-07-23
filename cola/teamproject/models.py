from django.db import models

# Create your models here.
class Group(models.Model):
    title = models.CharField(max_length=50)
    name1 = models.CharField(max_length=50, default='')
    name2 = models.CharField(max_length=50, default='')
    
    def __self__(self):
        return self.title
