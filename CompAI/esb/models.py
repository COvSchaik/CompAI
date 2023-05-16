from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class EscTemplate(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_esctemplates')
    date = models.DateTimeField(auto_now_add=True)    
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class EscTempQuestion(models.Model):
    template = models.ForeignKey(EscTemplate, on_delete=models.CASCADE, related_name = 'questions')
    number = models.IntegerField()
    answer = models.TextField(max_length=2000, null=True, blank=True)

class ESC(models.Model):
    date = models.DateTimeField(auto_now_add=True)    
    last_updated = models.DateTimeField(auto_now=True)
    
class ESCQuestion(models.Model):
    esc = models.ForeignKey(ESC, on_delete=models.CASCADE, related_name = 'questions')
    number = models.IntegerField()
    answer = models.TextField(max_length=2000, null=True, blank=True)