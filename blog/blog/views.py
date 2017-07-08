import logging
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader,context
from django.conf import settings
from blog.models import *
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
logger = logging.getLogger('blog.views')
def global_setting(request):
    return{
        'SITE_URL': settings.SITE_URL,
        'SITE_NAME': settings.SITE_NAME,
        'SITE_DESC': settings.SITE_DESC,
    }


def index(request):
    try:
        category_list = Category.objects.all()
        article_list = Article.objects.all()
        paginator = Paginator(article_list, 10)
        try:
            page = int(request.GET.get('page', 1))
            article_list = paginator.page(page)
        except(EmptyPage, InvalidPage, PageNotAnInteger):
            article_list = paginator.page(1)
    except Exception as e:
        logger.error(e)
    return render(request, "index.html", locals())




#def hello(request):
   #return render(request, "index.html", locals())
# Create your views here.
#def sayHello(request):
  #  s = 'hello world!'
  #  current_time=
#datetime.datetime.now()
  #  html ='<html><head></head><body><h1> %s </h1><p> %s </p></body><html> '% (s,current_time)
  #  return HttpResponse(html)