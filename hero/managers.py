from django.db import models

class AchievementManager(models.Manager):
  def active(self):
    import hero
    return self.get_query_set().filter(id__in=achievements.registered_achievements.keys())
    
    