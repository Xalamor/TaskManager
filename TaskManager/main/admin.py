from django.contrib import admin
from .models import Task, Chapter


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'task', 'chapter', 'visibility']


admin.site.register(Chapter)
