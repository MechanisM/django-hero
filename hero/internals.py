from django.contrib.auth.models import User
from django.db import models
from django.utils import importlib
from django.conf import settings
import imp
from hero.models import Achievement

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

def autodiscover():
  for app in settings.INSTALLED_APPS:
    # For each app, we need to look for an search_indexes.py inside that app's
    # package. We can't use os.path here -- recall that modules may be
    # imported different ways (think zip files) -- so we need to get
    # the app's __path__ and look for search_indexes.py on that path.

    # Step 1: find out the app's __path__ Import errors here will (and
    # should) bubble up, but a missing __path__ (which is legal, but weird)
    # fails silently -- apps that do weird things with __path__ might
    # need to roll their own index registration.
    try:
        app_path = importlib.import_module(app).__path__
    except AttributeError:
        continue

    # Step 2: use imp.find_module to find the app's search_indexes.py. For some
    # reason imp.find_module raises ImportError if the app can't be found
    # but doesn't actually try to import the module. So skip this app if
    # its search_indexes.py doesn't exist
    try:
        imp.find_module('achievements', app_path)
    except ImportError:
        continue

    # Step 3: import the app's search_index file. If this has errors we want them
    # to bubble up.
    importlib.import_module("%s.achievements" % app)