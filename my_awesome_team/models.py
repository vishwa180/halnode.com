from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Audit(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    class Meta:
        abstract = True


class Project(models.Model):
    name = models.CharField(max_length=32, null=False, blank=False, unique=True)
    is_active = models.BooleanField(default=True, null=False)

    def __str__(self):
        return self.name


class Entry(Audit):
    entry_types = [('Idea', 'Idea'), ('Task', 'Task Completion')]

    title = models.CharField(max_length=64, null=False, blank=True)
    type = models.CharField(max_length=12, null=False, choices=entry_types)
    project = models.ForeignKey(Project, on_delete=models.PROTECT)
    description = models.TextField(blank=True, null=True)
    tagged_users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='tagged_entries')

    def __str__(self):
        return self.title
