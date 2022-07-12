from django.contrib import admin
from . import models


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(models.Entry)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('created_by', 'title', 'created_at', 'project')
    list_filter = ('project', 'created_by')
    search_fields = ('title', 'description')
    filter_horizontal = ('tagged_users', )
