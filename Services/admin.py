from django.contrib import admin
from .models import URL

# Register your models here.

class URLAdmin(admin.ModelAdmin):
    list_display = ('user', 'target_url', 'alias', 'created_at') 
    list_filter = ('created_at',)  
    search_fields = ('user__username', 'alias')

admin.site.register(URL, URLAdmin)
