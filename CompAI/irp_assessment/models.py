from django.db import models
from projects.models import Project
from django.contrib.auth.models import User
from frameworks.models import Framework, FrameItem


# Create your models here.
class Assessment(models.Model):
    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True, related_name = 'assessments' )
    startdate = models.DateTimeField(auto_now_add=True)    
    last_updated = models.DateTimeField(auto_now=True)
    framework = models.ForeignKey(Framework, on_delete=models.CASCADE, related_name = 'assessments')
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_assessments')
    stage = models.CharField(max_length=100, default="design")

    def __str__(self):
        return self.name
    
class Item (models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name = 'items')
    item_count = models.IntegerField(null=True, blank=True)
    template = models.ForeignKey(FrameItem, on_delete=models.SET_NULL, null=True, blank=True, related_name = 'items')
    
    stage = models.CharField(max_length=100, default="design")
    saved = models.BooleanField(default=False)
    last_modified = models.DateTimeField(auto_now=True)   
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,) 

    maturity = models.IntegerField(null=True, blank=True)
    summary = models.TextField(max_length=2000, null=True, blank=True)
    proof = models.TextField(max_length=2000, null=True, blank=True)
    



