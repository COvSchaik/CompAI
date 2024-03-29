from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Template(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_templates')
    date = models.DateTimeField(auto_now_add=True)    
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class TempQuestion(models.Model):
    template = models.ForeignKey(Template, on_delete=models.CASCADE, related_name = 'questions')
    number = models.IntegerField()
    answer = models.TextField(max_length=2000, null=True, blank=True)

class SDS(models.Model):
    date = models.DateTimeField(auto_now_add=True)    
    last_updated = models.DateTimeField(auto_now=True)
    
class SDSQuestion(models.Model):
    sds = models.ForeignKey(SDS, on_delete=models.CASCADE, related_name = 'questions')
    number = models.IntegerField()
    answer = models.TextField(max_length=2000, null=True, blank=True)