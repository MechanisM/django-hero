from django.core.urlresolvers import reverse
from django.db import models
from datetime import *
from django.contrib.auth.models import User
from django.conf import settings
from hero import autodiscover
from hero.managers import AchievementManager
from hero.signals import achievement_unlocked

if hasattr(settings, 'ACHIEVEMENT_LEVEL_CHOICES'):
    LEVEL_CHOICES = settings.ACHIEVEMENT_LEVEL_CHOICES
else:
    LEVEL_CHOICES = (
        (1, "Bronze"),
        (2, "Silver"),
        (3, "Gold"),
        (4, "Diamond"),
    )

class Achievement(models.Model):
  id             = models.CharField(max_length=255, primary_key=True, editable=False, unique=True)
  title          = models.CharField(max_length=255)
  description    = models.TextField(null=False)
  points         = models.IntegerField(default=0, help_text="Points earned for unlocking this achievement.")
  secret         = models.BooleanField(default=0, help_text="The achievement is visible to a user but does not reveal its title, description, or points until the user has unlocked it")
  invisible      = models.BooleanField(default=0, help_text="The achievement is NOT visible to a user, untill unlocked")
  level          = models.IntegerField(default=1, choices=LEVEL_CHOICES) # Could make this a many to many field?
  image_locked   = models.ImageField(upload_to='achievements', default='achievements/images/default-locked.jpg')
  image_unlocked = models.ImageField(upload_to='achievements', default='achievements/images/default-unlocked.jpg')
  image_secret   = models.ImageField(upload_to='achievements', default='achievements/images/default-hidden.jpg')
  
  objects = AchievementManager()
  
  def image(self):
    return self.image_locked
  
  def unlock(self, **state):
    '''
    Unlock achievement for user if requirements are met
    '''
    user = state["user"]

    # Check if achievement can be unlocked
    unlock = self.unlock(**state)
    if unlock is None:
      return
    
    # Save
    unlocked_achievement, created = AchievementUnlocked.objects.get_or_create(achievement_id=self.id, user=user)
    
    if created is None:
      return # Already exists
    
    # Send signal
    achievement_unlocked.send(sender=self, achievement=unlocked_achievement)
  
  def is_unlocked(self, user):
    '''
    Check if achievement is already unlocked
    '''
    try:
      unlocked_achievement = AchievementUnlocked.objects.get(achievement_id=self.id, user=user)
    except AchievementUnlocked.DoesNotExists:
      return False # Not unlocked
    
    # Return unlocked achievement
    return unlocked_achievement  

class AchievementUnlocked(models.Model):
  achievement = models.ForeignKey(Achievement)
  user        = models.ForeignKey(User, related_name="achievements_unlocked")
  unlocked_at = models.DateTimeField(default=datetime.now)
  level       = models.IntegerField()