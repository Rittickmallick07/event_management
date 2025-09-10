from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'created_at')
    search_fields = ('name',)
from django.contrib import admin
from .models import Event

admin.site.register(Event)
