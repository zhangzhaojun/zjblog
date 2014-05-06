# -*- coding: utf-8 -*-
from django.contrib.sitemaps import Sitemap
from zjblog.models import Blog

class BlogSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Blog.objects.all()[:10]

    def lastmod(self, obj):
        return obj.pub_date

 
