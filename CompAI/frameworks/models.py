from django.db import models

# Create your models here.
class Framework(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class FrameItem(models.Model):
    framework = models.ForeignKey(Framework, on_delete=models.CASCADE, related_name='items')
    item_count = models.IntegerField(null=True, blank=True)
    item_nr = models.IntegerField(null=True, blank=True)
    stage = models.CharField(max_length=100, default="design")
    category = models.CharField(max_length=100, null=True, blank=True)
    respondent = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    deliverable_description = models.TextField(max_length=1000, null=True, blank=True)    

class FrameLevel(models.Model):
    item = models.ForeignKey(FrameItem, on_delete=models.CASCADE, related_name="levels")
    name = models.CharField(max_length=100)
    value = models.IntegerField()
    description = models.TextField(max_length=1000, null=True, blank=True)

