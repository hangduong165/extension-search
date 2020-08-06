from django.contrib import admin
from .models import Profile


# Register your models here.

class CustomProfile(admin.ModelAdmin):
    list_display = ['user', 'age']


admin.site.register(Profile, CustomProfile)
