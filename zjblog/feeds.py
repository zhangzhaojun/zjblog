# -*- coding: utf-8 -*-
from django.contrib.syndication.views import Feed
from zjblog.models import Blog

class LatestEntriesFeed(Feed):
    title = 'Zjblog feed'
    link = '/'
    description = u'Zjblog上最新的日志'

    def items(self):
        return Blog.objects.all()[:10]

    def item_title(self, item):
        return item.title

    
