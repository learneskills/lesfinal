from django.conf.urls import url
from .views import BlogList, BlogDetailView, TagIndexView, BlogCategoryDetailView

urlpatterns = [
    url(r'^$', BlogList.as_view(), name='blog'),
    url(r'^(?P<slug>[\w-]+)/$', BlogDetailView.as_view(), name='blog-detail'),
    url(r'category/(?P<slug>[\w-]+)/$', BlogCategoryDetailView.as_view(), name='blog_category_detail_view'),
    url(r'^tag/(?P<slug>[-\w]+)/$', TagIndexView.as_view(), name='blog_tagged'),
]