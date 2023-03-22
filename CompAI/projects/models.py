from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=100)
    startdate = models.DateTimeField()    
    enddate = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=100, default='active')
    description = models.TextField(max_length=200, null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_projects')
    members = models.ManyToManyField(User, related_name='projects')
    def __str__(self):
        return self.name