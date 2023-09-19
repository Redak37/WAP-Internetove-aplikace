from .models import *
from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import Permission


class MonitorLog(admin.ModelAdmin):
    """
    This class is used for Monitoring of changes made in administration interface.
    """
    list_display = ('action_time', 'user', 'content_type', 'object_repr', 'change_message', 'action_flag', )
    list_filter = ['action_time', 'user', 'content_type', 'action_flag']
    ordering = ('-action_time',)
    search_fields = ['object_repr', 'change_message']


admin.site.register(LogEntry, MonitorLog)
# Register your models here.

admin.site.register(Allergen)
admin.site.register(Product)
admin.site.register(Resource)
admin.site.register(ProductCategory)
admin.site.register(ProductResource)
admin.site.register(State)
admin.site.register(Order)
admin.site.register(ProductOrder)
admin.site.register(ResourceOrder)
admin.site.register(ResourceResOrder)
admin.site.register(Car)
admin.site.register(Permission)
