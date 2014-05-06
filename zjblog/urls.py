

from django.conf.urls import *
from zjblog.views import Details, Categorytoblogs, Blog_list, Tagtoblogs, showComments, weixin
from zjblog.feeds import LatestEntriesFeed
from zjblog.blogsitemap import BlogSitemap



sitemaps = { 'blog' : BlogSitemap }


    
    
urlpatterns = patterns('',
    #(r'^$', list_detail.object_list, category_info),
    (r'^$', Blog_list.as_view()),
    (r'^blog/(?P<pk>\d+)/$', Details.as_view()),
    (r'^category/(\d+)/$', Categorytoblogs.as_view()),
    (r'^latest/feed/$', LatestEntriesFeed()),
    (r'^tag/(?P<tag>[^/]+)/$', Tagtoblogs.as_view()),
    #(r'^tag/(?P<tag>\w+)/$', Tagtoblogs.as_view()),
    (r'^captcha/', include('captcha.urls')),
    (r'^postcomment/$', showComments),
    (r'^weixin/$', weixin),
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps }),
    # Example:
    # (r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    

    
)
