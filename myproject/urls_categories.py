from django.conf.urls import url, include
from .views import CategoryListView, CategoryDetailView, SingleProductDetailView, TopDiscountList, \
    RecentlyUpdatedList, blog, TagIndexView, AllCourse, email, success, course_model_form

urlpatterns = [
    url(r'^$', CategoryListView.as_view(), name='index'),
    url(r'^recently-updated-list/$', RecentlyUpdatedList.as_view(), name='recently_added'),
    url(r'^top-discount-list/$', TopDiscountList.as_view(), name='top_discount'),
    url(r'^all-courses/$', AllCourse.as_view(), name='all_course'),
    # url(r'contact/$', contact_us, name='contact'),
    url(r'^email/$', email, name='email'),
    url(r'^success/$', success, name='success'),
    url(r'^submit/$', course_model_form, name='submit'),

    url(r'^blog/$', blog, name='blog'),
    url(r'^tag/(?P<slug>[-\w]+)/$', TagIndexView.as_view(), name='tagged'),
    url(r'^(?P<slug>[\w-]+)/$', CategoryDetailView.as_view(), name='category_detail'),
    url(r'^(?P<pk>\d+)/(?P<slug>[-\w]+)/$', SingleProductDetailView.as_view(), name='single-product'),


]
