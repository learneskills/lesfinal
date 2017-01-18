from django.conf.urls import url
from .views import BlogList, BlogDetailView

urlpatterns = [
    url(r'^$', BlogList.as_view(), name='blog'),
    url(r'^(?P<slug>[\w-]+)/$', BlogDetailView.as_view(), name='blog-detail'),
]