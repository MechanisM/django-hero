from django.conf import settings

ACHIEVEMENT_LEVELS         = getattr(settings, 'ACHIEVEMENT_LEVELS', ((1, "Bronze"), (2, "Silver"), (3, "Gold"),(4, "Diamond"),))
ACHIEVEMENT_IMAGE_LOCKED   = getattr(settings, 'ACHIEVEMENT_IMAGE_LOCKED', 'achievements/images/default-locked.jpg')
ACHIEVEMENT_IMAGE_UNLOCKED = getattr(settings, 'ACHIEVEMENT_IMAGE_UNLOCKED', 'achievements/images/default-unlocked.jpg')
ACHIEVEMENT_IMAGE_SECRET   = getattr(settings, 'ACHIEVEMENT_IMAGE_SECRET', 'achievements/images/default-secret.jpg')