from django.contrib import admin
from .models import Region,County,Sub_County,School,Learner

# Register your models here.
admin.site.register(Region)
admin.site.register(County)
admin.site.register(Sub_County)
admin.site.register(School)
admin.site.register(Learner)