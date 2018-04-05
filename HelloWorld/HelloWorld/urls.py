"""HelloWorld URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from . import view
from HelloWorld.testdb import testdb
from HelloWorld import search
from HelloWorld import search2
from TestModel import models
from django.views.generic.base import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    url('hello/', view.hello),
    url('^testdb/$', testdb),
    url('^search_form/$', search.search_form),
    url('^search/$', search.search),
    url('^search_post/$', search2.search_post),
    url('^contact/$', view.contact),
    url('^time/$', view.current_datetime),
    url(r'^time/plus/(?P<offset>\d{1,2})/$', view.hours_ahead),
    url('^foo/$', view.foobar_view, {'template_name': 'foo_view.html'}),
    url('^bar/$', view.foobar_view, {'template_name': 'bar_view.html'}),
    url(r'^publishers/$', view.object_list, {'model': models.Publisher}),
    url(r'^books/$', view.object_list, {'model': models.Book}),
    url(r'^about/$', TemplateView.as_view(template_name="about.html")),
    url(r'^about/(?P<page>\w+)/$', view.AboutView.as_view()),
    url(r'^publisherlist/$', view.PublisherList.as_view()),
    url(r'^publisherdetail/(?P<pk>[0-9]+)/$', view.PublisherDetailView.as_view()),
    url(r'^csv/$', view.some_csv_view),
    url(r'^scsv/$', view.some_streaming_csv_view),
    url(r'^tcsv/$', view.some_template_view),
    url(r'^pcsv/$', view.some_pdf_view),
    url(r'^p2csv/$', view.some_pdf2_view),
]
