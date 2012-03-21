from django.contrib import admin
from hero.models import *
from django import forms

class AchievementAdmin(admin.ModelAdmin):
    #fields = ('id',)
    list_display = ('title', 'description')
    readonly_fields = ('title', 'description', 'id', 'secret', 'points', 'invisible', 'level', 'image_locked','image_unlocked', 'image_secret',)

admin.site.register(Achievement, AchievementAdmin)