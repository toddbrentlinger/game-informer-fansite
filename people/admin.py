from django.contrib import admin
from .models import Person, Staff, StaffPosition, StaffPositionInstance

# Inlines

class StaffPositionInstanceInline(admin.TabularInline):
    model = StaffPositionInstance
    extra = 0

# Register your models here.

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('full_name',)}

@admin.register(StaffPosition)
class StaffPositionAdmin(admin.ModelAdmin):
    search_fields = ['title']
    inlines = [StaffPositionInstanceInline,]

@admin.register(StaffPositionInstance)
class StaffPositionInstanceAdmin(admin.ModelAdmin):
    list_filter = ('position__title',)
    search_fields = ['staff__person__full_name', 'staff__person__short_name', 'position__title']

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    search_fields = ['person__full_name']
    inlines = [StaffPositionInstanceInline,]