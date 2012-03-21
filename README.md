Django Hero
=========

Hero is a powerful, extensible, reusable application that provides
support for awarding "Achievements" to users in Django.

Installation
------------

Add hero to your INSTALLED_APPS:

    INSTALLED_APPS = [
      # ...
      "hero",
    ]

Add the autodiscover function to your urls.py for your convenience.

    # Register achievements
    import hero
    hero.autodiscover()

Optional: Hook up hero to your URLconf for some default views.

    urlpatterns = patterns("",
      # ...
      url(r"^achievements/", include("hero.urls"))
    )

SETTINGS
------------

ACHIEVEMENT_LEVEL_CHOICES

default:  Bronze, Silver, Gold, Diamond

USAGE
------------

Start by creating a achievements.py file in your app/project. The autodiscover function will pick this up.
Here you will define your custom achievements.

A achievement object might look like this:

    from hero import achievements
    
    class TestAchievement(object):
      '''
      Achievement attribute's
      '''
      id          = "comments_50"
      points      = 500
      title       = "50 comments ja"
      description = "User has posted 50 comments"
      secret      = False
      hidden      = False
      image_locked   = 'achievements/images/default-locked.jpg'
      image_unlocked = 'achievements', default='achievements/images/default-unlocked.jpg'
      image_secret   = 'achievements/images/default-hidden.jpg'
  
      '''
      Event's on wich this achievement should be called
      '''
      events = [
        "points_awarded",
      ]
      
      def validate_unlock(self, **state):
        '''
        Validates unlock requirements
        '''
        user = state["user"]
        points = 5000
        if points == 5000:
          return AchievementUnlocked()
    
    # Register te achievement
    achievements.register(TestAchievement)

There are a few relevant attributes and methods here.

*   attribute:: id

    The unique identifier for the 'Achievement', it should never change.
    
*   attribute:: title

    Title for this achievement

*   attribute:: description

    Description for this achievement

*   attribute:: secret

    Secret achievement flag.Secret achievements should not be revealed untill a user unlocked it.

*   attribute:: hidden

    Hidden achievement flag. Hidden achievements should not be revealed untill a user unlocked it, neither does it shows as a secret achievement in listings.
    
*   attribute:: image_locked

    Override locked achievement default image

*   attribute:: image_unlocked

    Override unlocked achievement default image

*   attribute:: image_secret

    Override hidden achievement default image  

Achievement's are saved to the DB. This way you can use Django's ORM to query your achievements.

- Sjoerd Arendsen

