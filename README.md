zjblog
======
zjblog是一个博客程序，采用mysql数据库，基于django搭建。

依赖文件(需要安装)：

	django1.6
	django-taggit
	django-mptt
	django-simple-captcha

zjblog的安装方法：

1、settings.py文件中如下设置：

	INSTALLED_APPS = (
    			...
    			'zjblog',
    	)

2、mysite目录下的urls.py中，如下设置：

urlpatterns = patterns('',

    ...
    (r'^blogs/', include('zjblog.urls')),
    ...
)

许可声明：

	The MIT License (MIT)
	Copyright (c) 2014 zhangzhaojun
