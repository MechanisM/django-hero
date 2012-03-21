from django.contrib import admin
from hero.models import *
from django import forms

class AchievementAdmin(admin.ModelAdmin):
  list_display = ('title', 'description', 'secret', 'invisible',)
  readonly_fields = ('title', 'description', 'id', 'secret', 'invisible', 'image_locked', 'image_unlocked', 'image_secret',)

admin.site.register(Achievement, AchievementAdmin)