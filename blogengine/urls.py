from django.conf.urls import patterns, url
from django.views.generic import ListView, DetailView
from blogengine.models import Post

urlpatterns = patterns('',
        url(r'^(?P<page>\d+)?/?$', ListView.as_view(
            model=Post,
            paginate_by=5,
        )),

        url(r'^(?P<pub_date__year>\d{4})/(?P<pub_date__month>\d{1,2})/(?P<pub_date__day>\d{1,2})/(?P<slug>[a-zA-Z0-90]+)/?$',  DetailView.as_view(
            model=Post,
        )),
)
