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

Optional: Hook up hero to your URLconf for some default views

    urlpatterns = patterns("",
      # ...
      url(r"^achievements/", include("hero.urls"))
    )

USAGE
------------


- Sjoerd Arendsen

