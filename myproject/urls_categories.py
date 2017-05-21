from django.conf.urls import url

from .views import CategoryDetailView, SingleProductDetailView, TopDiscountList, \
    RecentlyUpdatedList, TagIndexView, AllCourse, email, success, course_model_form, CourseProviderStore

urlpatterns = [
    # Course URLS

    url(r'^recently-updated-list/$', RecentlyUpdatedList.as_view(), name='recently_added'),
    url(r'^top-discount-list/$', TopDiscountList.as_view(), name='top_discount'),

    url(r'^email/$', email, name='email'),
    url(r'^success/$', success, name='success'),
    url(r'^submit/$', course_model_form, name='submit'),

    # Course URLS
    url(r'^(?P<slug>[\w-]+)/$', CategoryDetailView.as_view(), name='category_detail'),
    url(r'^(?P<pk>\d+)/(?P<slug>[-\w]+)/$', SingleProductDetailView.as_view(), name='single-product'),
    url(r'^provider/(?P<slug>[\w-]+)/$', CourseProviderStore.as_view(), name='provider'),
    url(r'^tag/course/(?P<slug>[-\w]+)/$', TagIndexView.as_view(), name='tagged'),

]
