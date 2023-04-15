from django.contrib import admin
from .models import Framework, FrameItem, FrameLevel

# Register your models here.
admin.site.register(Framework)
admin.site.register(FrameItem)
admin.site.register(FrameLevel)