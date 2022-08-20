from django.contrib import admin
from .models import Show

@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    pass
