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
      level       = 1
      points      = 500
      title       = "50 comments ja"
      description = "User has posted 50 comments"
      secret      = 0
  
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

    The unique identifier for this 'Achievement', it should never change.

- Sjoerd Arendsen

