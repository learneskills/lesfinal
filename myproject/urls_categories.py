from django.conf.urls import url
from .views import CategoryListView, CategoryDetailView, SingleProductDetailView, TopDiscountList, \
    RecentlyUpdatedList, blog, TagIndexView, AllCourse, email, success, course_model_form
from books.views import AllBook, RecentlyUpdatedBookList, TopDiscountBookList, SingleBookDetailView, TagIndexBookView, BookCategoryDetailView

urlpatterns = [
    # Course URLS
    url(r'^$', CategoryListView.as_view(), name='index'),
    url(r'^recently-updated-list/$', RecentlyUpdatedList.as_view(), name='recently_added'),
    url(r'^top-discount-list/$', TopDiscountList.as_view(), name='top_discount'),
    url(r'^all-course/$', AllCourse.as_view(), name='all_course'),

    # Books URLS
    url(r'^recently-updated-books-list/$', RecentlyUpdatedBookList.as_view(), name='recently_added_book_list'),
    url(r'^top-discount-books-list/$', TopDiscountBookList.as_view(), name='top_discount_book_list'),
    url(r'^all-books/$', AllBook.as_view(), name='all_books'),

    # url(r'contact/$', contact_us, name='contact'),
    url(r'^email/$', email, name='email'),
    url(r'^success/$', success, name='success'),
    url(r'^submit/$', course_model_form, name='submit'),
    url(r'^blog/$', blog, name='blog'),

    # Course URLS
    url(r'^(?P<slug>[\w-]+)/$', CategoryDetailView.as_view(), name='category_detail'),
    url(r'^(?P<pk>\d+)/(?P<slug>[-\w]+)/$', SingleProductDetailView.as_view(), name='single-product'),

    # Books URL
    url(r'^(?P<slug>[\w-]+)/$', BookCategoryDetailView.as_view(), name='book_category_detail'),
    url(r'^book/(?P<slug>[-\w]+)/$', SingleBookDetailView.as_view(), name='single-book-detail'),

    # Tag URL - Course & Books
    url(r'^tag/(?P<slug>[-\w]+)/$', TagIndexBookView.as_view(), name='book-tagged'),
    url(r'^tag/(?P<slug>[-\w]+)/$', TagIndexView.as_view(), name='tagged'),

]
