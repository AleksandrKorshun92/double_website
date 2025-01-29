from django.contrib import admin
from .models import BaseSites


@admin.register(BaseSites)
class MyModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'url_sites']  
    search_fields = ['title']            
