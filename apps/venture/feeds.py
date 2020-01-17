from django.contrib.syndication.views import Feed
from django.urls import reverse
from apps.venture.models import Venture

class RssVenturesFeed(Feed):
    title = "Projets"
    link = "/ventures/rss/"
    description = "Flux des nouveaux projets."

    def items(self):
        return Venture.objects.all()[:5]

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.description