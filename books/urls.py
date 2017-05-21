from django.conf.urls import url
from books.views import AllBook, RecentlyUpdatedBookList, TopDiscountBookList, SingleBookDetailView, TagIndexBookView, \
    BookCategoryDetailView

urlpatterns = [

    # Books URLS
    url(r'^recently-updated-books-list/$', RecentlyUpdatedBookList.as_view(), name='recently_added_book_list'),
    url(r'^top-discount-books-list/$', TopDiscountBookList.as_view(), name='top_discount_book_list'),
    url(r'^all-books/$', AllBook.as_view(), name='all_books'),


    # Books URL
    url(r'^(?P<slug>[\w-]+)/$', BookCategoryDetailView.as_view(), name='book_category_detail'),
    url(r'^(?P<pk>\d+)/(?P<slug>[-\w]+)/$', SingleBookDetailView.as_view(), name='single-book-detail'),

    # Tag URL - Course & Books
    url(r'^tag/book/(?P<slug_book>[-\w]+)/$', TagIndexBookView.as_view(), name='book-tagged'),

]
