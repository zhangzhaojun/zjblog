# -*- coding: utf-8 -*-

from django.core.context_processors import csrf
from django.shortcuts import render_to_response, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.list import ListView
from django.views.generic import DetailView
from zjblog.models import Blog, Category, FriendLink, BaseInformation, ZComments
from django.conf import settings
from django.contrib.sites.models import Site
#from django.contrib import comments
from captcha.fields import CaptchaField#m
from django.utils.encoding import smart_str, smart_unicode
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django import forms #m
import xml.etree.ElementTree as ET
import random
import hashlib, re, time



class Blog_list(ListView):
        base_information = BaseInformation.objects.get(pk=1)
        queryset = Blog.objects.all()
        paginate_by = 5
        context_object_name = "blog_list"
        template_name = base_information.my_template+"/blog_list.html"

        def get_context_data(self, **kwargs):
                                
                allcomments = ZComments.objects.all()
                recent_comment = allcomments.order_by('-pub_date')[0:10]
                
                
                context = super(Blog_list, self).get_context_data(**kwargs)
                
                context['category_list'] = Category.objects.all()
                context['tag_list'] = Blog.tags.all()
                context['fls'] = FriendLink.objects.all()
                context['recent_comment'] = recent_comment
                context['base_information'] = self.base_information
                return context
                
class CommentsForm(forms.Form):#m
        
        author = forms.CharField(label=u'名称（必填）', required=True)
        e_mail = forms.EmailField(label=u'邮箱（必填）', required=True)
        url = forms.URLField(label=u'链接（可选）', required=False)
        commentbox = forms.CharField(label=u'内容（必填）', widget=forms.Textarea, required=True)        
        captcha = CaptchaField(label=u'验证码（必填）')

class Details(DetailView):
        context_object_name = 'post'
        base_information = BaseInformation.objects.get(pk=1)
        template_name = base_information.my_template+"/detail.html"
        form = CommentsForm()
        
        def get_queryset(self):
                return  Blog.objects.filter(pk = self.kwargs['pk'])
        def get_context_data(self, **kwargs):
             context = super(Details, self).get_context_data(**kwargs)
             blog = Blog.objects.get(pk = self.kwargs['pk'])
             #增加内容开始
             upid = 0
             nextid = 0
             upblog = ''
             nextblog = ''
             #增加内容结束
             
             post_tags = blog.tags.names()
             r_objects = blog.tags.similar_objects()
             blog.hotcount = blog.hotcount + 1
             blog.save()
             #增加内容开始
             lastpost = Blog.objects.latest('pub_date')
             if blog.id > 1 :
                     upid = blog.id - 1
                     upblog = Blog.objects.get(pk=upid)
             if blog.id < lastpost.id :
                     nextid = blog.id + 1
                     nextblog = Blog.objects.get(pk=nextid)
             #增加内容结束
             
             if len(r_objects) > 10:
                    r_objects = random.sample(r_objects, 10)
             context['category_list'] = Category.objects.all()
             #context['tag_list'] = Blog.tags.all()
             #context['fls'] = FriendLink.objects.all()
             nodes = ZComments.objects.filter(r_blog = blog)
             counts = 0
             for count in nodes:
                     counts = counts + 1
             blog.commentcount = counts
             blog.save()
             context['nodes'] = nodes
             context['similar'] = r_objects
             context['tags'] = post_tags
             context['base_information'] = self.base_information
             context['upid'] = upid
             context['nextid'] = nextid
             context['upblog'] = upblog
             context['nextblog'] = nextblog
             context['form'] = self.form
             return context         
    


class Categorytoblogs(ListView):
        base_information = BaseInformation.objects.get(pk=1)
        template_name = base_information.my_template+"/ctob.html"
        paginate_by = 5
        
        
        def get_queryset(self):
                
                c = Category.objects.get(pk=self.args[0])
                return Blog.objects.filter(category = c)

        def get_context_data(self, **kwargs):
                allcomments = ZComments.objects.all()
                recent_comment = allcomments.order_by('-pub_date')[0:10]
                
                context = super(Categorytoblogs, self).get_context_data(**kwargs)
                
                context['category_list'] = Category.objects.all()
                context['tag_list'] = Blog.tags.all()
                context['fls'] = FriendLink.objects.all()
                context['recent_comment'] = recent_comment
                context['cid'] = self.args[0]
                context['base_information'] = self.base_information
                return context        

class Tagtoblogs(ListView):
        base_information = BaseInformation.objects.get(pk=1)
        template_name = base_information.my_template+'/ttob.html'
        paginate_by = 5
        context_object_name = "blog_list"

        def get_queryset(self):
                return Blog.objects.filter(tags__name__in = [self.kwargs['tag']])

        def get_context_data(self, **kwargs):
                allcomments = ZComments.objects.all()
                recent_comment = allcomments.order_by('-pub_date')[0:10]
                
                context = super(Tagtoblogs, self).get_context_data(**kwargs)
                
                context['category_list'] = Category.objects.all()
                context['tag_list'] = Blog.tags.all()
                context['fls'] = FriendLink.objects.all()
                context['recent_comment'] = recent_comment
                context['blog_tag'] = self.kwargs['tag']
                context['base_information'] = self.base_information
                return context



def showComments(request):
        base_information = BaseInformation.objects.get(pk=1)
        template_name = base_information.my_template+"/test.html"
        if request.method == 'POST':
                form = CommentsForm(request.POST)
                pid = request.POST['parent_id']
                bid = request.POST['blog_id']
                if form.is_valid():
                        r_blog = Blog.objects.get(pk = request.POST['blog_id'])
                        if request.POST['parent_id'] != '':
                                r_comment = ZComments.objects.get(pk = request.POST['parent_id'])
                                r_comment.save()#这里一定要调用save方法，否则会出现"cannot assign instance is on database "default",value is on database "slave"的错误
                                comment = ZComments(r_blog = r_blog, c_author = request.POST['author'], e_mail = request.POST['e_mail'], url = request.POST['url'], content = request.POST['commentbox'], parent = r_comment)
                        else:
                                comment = ZComments(r_blog = r_blog, c_author = request.POST['author'], e_mail = request.POST['e_mail'], url = request.POST['url'], content = request.POST['commentbox'])
                        comment.save()
                
                        return HttpResponseRedirect('/blogs/blog/'+str(r_blog.id)+'/#c'+str(comment.id))
                #else:
                        #form = CommentsForm()
                return render(request, template_name, { 'form':form, 'blog_id':bid, 'parent_id':pid, })
                

#微信公众平台
@csrf_exempt
def weixin(request):
        
        if request.method =='GET':
                echostr = request.GET.get('echostr')
                boolvalue = checkSignature(request)
                if boolvalue:
                        return HttpResponse(echostr)
                
        if request.method == 'POST':
                response = HttpResponse(response_msg(request))
                return response
                
                #return HttpResponse('123')       
                        
                
        

def checkSignature(request):
        token = 'zzj'
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')
        

        tmpList = [token, timestamp, nonce]
        
        tmpList.sort()
        tmpstr = "%s%s%s" % tuple(tmpList)
        hashstr = hashlib.sha1(tmpstr).hexdigest()
        
        if hashstr == signature:
                return True
        else:
                return None

def parse_request_xml(rootElem):
        msg = {}
        if rootElem.tag == 'xml':
                for child in rootElem:
                        msg[child.tag] = smart_str(child.text)
        return msg

def response_msg(request):
        rawStr = smart_str(request.raw_post_data)
        msg = parse_request_xml(ET.fromstring(rawStr))
        msgType = msg.get("MsgType")
        msgContent = msg.get("Content")
        response_msg = u"您所发送的请求错误！"
        if msgType == "text":
                if msgContent == "r":
                        response_msg = u'<a href="http://zhangzhaojun.sinaapp.com">您好，点此阅读z系内容</a>'
                else:
                        response_msg = u"z系微信操作指南：\n\n发送字母r，进入浏览器阅读模式"
        if msgType == "event":
                if msg.get("Event") == "subscribe":
                        response_msg = u"欢迎来到z系！z系微信操作指南：\n\n发送字母r，进入浏览器阅读模式"
                        
        return pack_text_xml(msg, response_msg)

def pack_text_xml(post_msg,response_msg):
	text_tpl = '''<xml>
				<ToUserName><![CDATA[%s]]></ToUserName>
				<FromUserName><![CDATA[%s]]></FromUserName>
				<CreateTime>%s</CreateTime>
				<MsgType><![CDATA[%s]]></MsgType>
				<Content><![CDATA[%s]]></Content>
				</xml>'''
	text_tpl = text_tpl % (post_msg['FromUserName'],post_msg['ToUserName'],str(int(time.time())),'text',response_msg)
	# 调换发送者和接收者，然后填入需要返回的信息到xml中
	return text_tpl
#微信公众平台结束      
        
        
