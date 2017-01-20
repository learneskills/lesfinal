from django.conf.urls import url
from .views import BlogList, BlogDetailView, TagIndexView

urlpatterns = [
    url(r'^$', BlogList.as_view(), name='blog'),
    url(r'^(?P<slug>[\w-]+)/$', BlogDetailView.as_view(), name='blog-detail'),
    url(r'^tag/blog/(?P<slug>[-\w]+)/$', TagIndexView.as_view(), name='blog_tagged'),
]