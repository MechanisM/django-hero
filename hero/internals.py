from django.contrib.auth.models import User
from django.db import models
from hero.models import Achievement
from sorl.thumbnail import ImageField

class AchievementRegistery(object):
    def __init__(self):
      self._event_registry = {} # holds events to achievements relationships
    
    def register(self, achievement):
      '''
      Build event registery
      '''
      self._to_db(achievement)
      for event in achievement.events:
        self._event_registry.setdefault(event, []).append(achievement.id)
      
    def _to_db(self, achievement):
      '''
      Save a achievement to the DB, so we can use django's ORM
      '''
      achievement_db, created = Achievement.objects.get_or_create(id=achievement.id)
      
      # Fill in field value's
      for field in achievement_db._meta.fields:
        if hasattr(achievement, field.name):
          setattr(achievement_db, str(field.name), getattr(achievement, field.name))
        else:
          setattr(achievement_db, str(field.name), field.default)  
      
      achievement_db.save()
    
    def unlock(self, event, **state):
      '''
      Run through the achievements for a event
      '''
      for achievement_id in self._event_registry[event]:
        achievement = Achievement.objects.get(id=achievement_id)
        achievement.unlock(**state)

achievements = AchievementRegistery()