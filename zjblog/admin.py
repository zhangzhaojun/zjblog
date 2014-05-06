# -*- coding: utf-8 -*-
from zjblog.models import Blog, Category, FriendLink, BaseInformation, ZComments
from django.contrib import admin


#注册需要后台管理的类        
admin.site.register(Blog)
admin.site.register(Category)
admin.site.register(FriendLink)
admin.site.register(BaseInformation)
admin.site.register(ZComments)
