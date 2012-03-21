from django.conf.urls.defaults import patterns, include, url
from django.views.generic.list_detail import *
from django.views.generic import ListView
from django.views.decorators.cache import cache_page
from hero.models import Achievement

urlpatterns = patterns('',
  url(r'^all.html$', ListView.as_view(
              queryset=Achievement.objects.all(),
              context_object_name='listObject',
              template_name='hero/achievements.html')),
)