from django.contrib.auth.models import User
from django.db import models
from django.utils import importlib
from django.conf import settings
import imp
from hero.settings import *
from hero.models import Achievement

class AchievementRegistery(object):
  def __init__(self):
    self._registry = {}
    self._event_registry = {} # holds events to achievements relationships
  
  def register(self, achievement):
    achievement = achievement()
    self._registry[achievement.id] = achievement
    for event in achievement.events:
       self._event_registry.setdefault(event, []).append(achievement.id)
       
    self._to_db(achievement)
    return achievement
      
  def _to_db(self, achievement):
    '''
    Save a achievement to the DB, so we can use django's ORM
    '''
    achievement_db, created = Achievement.objects.get_or_create(id=achievement.id)
      
  def unlock(self, event, **state):
    '''
    Run unlock methods for given event
    '''
    unlocks = {}
    user    = state["user"]

    for achievement_id in self._event_registry[event]:
       achievement = Achievement.objects.get(id=achievement_id)
       unlocked = achievement.unlock(**state)
    
    return  
      
achievements = AchievementRegistery()

class AchievementMetaClass(type):
  def __new__(cls, name, bases, attrs):
    achievement = super(AchievementMetaClass, cls).__new__(cls, name, bases, attrs)
    parents = [b for b in bases if isinstance(b, AchievementMetaClass)]
    if not parents:
        # If this isn't a subclass of AchievementMeta, don't do anything special.
        return achievement
        
    return achievements.register(achievement)

class AchievementMeta(object):
  __metaclass__ = AchievementMetaClass
  
  secret         = False
  invisible      = False
  image_locked   = ACHIEVEMENT_IMAGE_LOCKED
  image_unlocked = ACHIEVEMENT_IMAGE_UNLOCKED
  image_secret   = ACHIEVEMENT_IMAGE_SECRET

def autodiscover():
  for app in settings.INSTALLED_APPS:
    try:
        app_path = importlib.import_module(app).__path__
    except AttributeError:
        continue

    try:
        imp.find_module('achievements', app_path)
    except ImportError:
        continue

    importlib.import_module("%s.achievements" % app)