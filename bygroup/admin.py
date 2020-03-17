from django.contrib import admin
from .models import SClist, Metadata


class SClistAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'number')


class MetadataAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'value')


admin.site.register(SClist, SClistAdmin)
admin.site.register(Metadata, MetadataAdmin)
