from django.contrib import admin
from .models import Template, TempQuestion, SDS, SDSQuestion

# Register your models here.
admin.site.register(SDS)
admin.site.register(SDSQuestion)
admin.site.register(Template)
admin.site.register(TempQuestion)