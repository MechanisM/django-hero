from django.contrib import admin
from hero.models import *
from django import forms

class AchievementAdmin(admin.ModelAdmin):
  list_display = ('title', 'description',)
  readonly_fields = ('title', 'description',)

admin.site.register(Achievement, AchievementAdmin)