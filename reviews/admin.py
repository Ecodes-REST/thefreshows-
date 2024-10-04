from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'description','rating', 'rated_at', 'rate_updated_at']
    autocomplete_fields = ['user']
    list_editable = ['rating']


    