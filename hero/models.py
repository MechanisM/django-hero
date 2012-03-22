from django.core.urlresolvers import reverse
from django.db import models
from datetime import *
from django.contrib.auth.models import User
from django.conf import settings
from hero.managers import AchievementManager
from hero.signals import achievement_unlocked

if hasattr(settings, 'ACHIEVEMENT_LEVELS'):
  LEVEL_CHOICES = settings.ACHIEVEMENT_LEVELS
else:
  LEVEL_CHOICES = (
      (1, "Bronze"),
      (2, "Silver"),
      (3, "Gold"),
      (4, "Diamond"),
  )

class Achievement(models.Model):
  id = models.CharField(max_length=255, editable=False, primary_key=True, unique=True)
  #title          = models.CharField(max_length=255)
  #description    = models.TextField(null=False)
  #secret         = models.BooleanField(default=0, help_text="The achievement is visible to a user but does not reveal its title, description, or points until the user has unlocked it")
  #invisible      = models.BooleanField(default=0, help_text="The achievement is NOT visible to a user, untill unlocked")
  #image_locked   = models.ImageField(upload_to='achievements', default='achievements/images/default-locked.jpg')
  #image_unlocked = models.ImageField(upload_to='achievements', default='achievements/images/default-unlocked.jpg')
  #image_secret   = models.ImageField(upload_to='achievements', default='achievements/images/default-hidden.jpg')
  #meta_object    = PickledObjectField()
  
  objects = AchievementManager()
  
  @property
  def meta_achievement(self):
    from hero import achievements
    return achievements._registry[self.id]
  
  @property
  def title(self):
    return self.meta_achievement.title
  
  @property
  def description(self):
    return self.meta_achievement.description
  
  def unlock(self, **state):
    '''
    Unlock achievement for user if requirements are met
    '''
    user = state["user"]
    
    # Check if achievement can be unlocked
    unlock = self.meta_achievement.unlock(**state)
    if unlock is None:
      return
    
    if AchievementUnlocked.objects.filter(achievement=self, user=user):
      return # already there
    
    # Save
    unlocked_achievement = AchievementUnlocked.objects.create(achievement=self, user=user, level=unlock.level)

    # Send signal
    achievement_unlocked.send(sender=self, achievement=unlocked_achievement)
    
    return unlocked_achievement
  
  def image(self):
    return self.meta_achievement.image_locked
  
  def is_unlocked(self, user):
    '''
    Check if achievement is already unlocked
    '''
    try:
      unlocked_achievement = AchievementUnlocked.objects.get(achievement_id=self.id, user=user)
    except AchievementUnlocked.DoesNotExists:
      return # Not unlocked
    
    # Return unlocked achievement
    return unlocked_achievement

class AchievementUnlocked(models.Model):
  achievement = models.ForeignKey(Achievement)
  user        = models.ForeignKey(User, related_name="achievements_unlocked")
  unlocked_at = models.DateTimeField(default=datetime.now)
  level       = models.IntegerField()
