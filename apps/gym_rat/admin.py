from django.contrib import admin
from .models import Exercise

class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

admin.site.register(Exercise, ExerciseAdmin)