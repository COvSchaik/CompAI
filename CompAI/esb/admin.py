from django.contrib import admin
from .models import EscTemplate, EscTempQuestion, ESC, ESCQuestion

# Register your models here.
admin.site.register(ESC)
admin.site.register(ESCQuestion)
admin.site.register(EscTemplate)
admin.site.register(EscTempQuestion)