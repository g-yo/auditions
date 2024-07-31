from django.contrib import admin
from .models import *

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'gender', 'number_of_people', 'location')

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('movie', 'name', 'email', 'phone', 'age', 'gender')

admin.site.register(CustomUser)
