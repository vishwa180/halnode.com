from django.contrib import admin
from .models import ContactMessage, Lead
# Register your models here.


class LeadAdmin(admin.ModelAdmin):
    list_display = ('email', 'done')
    list_filter = ('done',)
    search_fields = ('email',)


admin.site.register(ContactMessage, LeadAdmin)
admin.site.register(Lead, LeadAdmin)
