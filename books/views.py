import random

from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.list import ListView
from taggit.models import Tag

from blog.models import BlogDetail
from books.models import BookMainCategory, BookCategory, BookDetail
from myproject.forms import ContactForm
from webproject import settings
from hitcount.views import HitCountDetailView
from myproject.models import Course_detail


# Create your views here.


class TagMixin(object):
    def get_context_data(self, **kwargs):
        context = super(TagMixin, self).get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        return context


class SingleBookDetailView(TagMixin, HitCountDetailView):
    model = BookDetail
    count_hit = True
    queryset = BookDetail.objects.all()
    template_name = 'books/single_book_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SingleBookDetailView, self).get_context_data(**kwargs)
        context.update({
            'main_category': BookMainCategory.objects.all(),
            'recently_updated': BookDetail.objects.order_by('-id').distinct()[:10],
            'top_discount': BookDetail.objects.order_by('-discount').filter(discount__range=(0, 99)).distinct()[:10],
            'blog_tags': BlogDetail.tags.all(),
            'book_tags': BookDetail.tags.all(),
            'course_tags': Course_detail.tags.all(),
            'recently_course_footer': Course_detail.objects.order_by('-id').filter(discount__range=(0, 99)).distinct()[
                                      :5],
            'discount_course_footer': Course_detail.objects.order_by('-discount').filter(
                discount__range=('1', '99')).distinct()[:5],
            'blog_footer': BlogDetail.objects.all().distinct()[:5],
        })
        instance = self.get_object()
        context["related"] = sorted(BookDetail.objects.get_related(instance).distinct()[:10],
                                    key=lambda x: random.random())
        return context


class TagIndexBookView(TagMixin, ListView):
    model = BookDetail
    queryset = BookDetail.objects.all()
    template_name = 'books/tag_book_detail.html'

    def get_queryset(self):
        return BookDetail.objects.filter(tags__slug=self.kwargs.get('slug_book'))

    def get_context_data(self, **kwargs):
        context = super(TagIndexBookView, self).get_context_data(**kwargs)
        context.update({
            'main_category': BookMainCategory.objects.all(),
            'category': BookCategory.objects.all(),
            'recently_updated': BookDetail.objects.order_by('-id').distinct()[:3],
            'top_discount': BookDetail.objects.order_by('-discount').distinct()[:3],
            'blog_tags': BlogDetail.tags.all(),
            'book_tags': BookDetail.tags.all(),
            'course_tags': Course_detail.tags.all(),
            'recently_course_footer': Course_detail.objects.order_by('-id').filter(discount__range=(0, 99)).distinct()[
                                      :5],
            'discount_course_footer': Course_detail.objects.order_by('-discount').filter(
                discount__range=('1', '99')).distinct()[:5],
            'blog_footer': BlogDetail.objects.all().distinct()[:5],
        })
        return context


class BookCategoryListView(ListView):
    model = BookCategory
    paginate_by = 4
    template_name = 'index.html'
    context_object_name = 'category_list'

    def get_context_data(self, **kwargs):
        context = super(BookCategoryListView, self).get_context_data(**kwargs)

        context.update({
            'course_detail_discount_list': BookDetail.objects.order_by('-discount').distinct()[:6],
            'course_detail_recently_updated_list': BookDetail.objects.order_by('-pk').distinct()[:4],
            'course_all': BookDetail.objects.order_by('-title'),
            'main_category': BookMainCategory.objects.all(),
            'blog_tags': BlogDetail.tags.all(),
            'book_tags': BookDetail.tags.all(),
            'course_tags': Course_detail.tags.all(),
            'recently_course_footer': Course_detail.objects.order_by('-id').filter(discount__range=(0, 99)).distinct()[
                                      :5],
            'discount_course_footer': Course_detail.objects.order_by('-discount').filter(
                discount__range=('1', '99')).distinct()[:5],
            'blog_footer': BlogDetail.objects.all().distinct()[:5],
        })
        return context

    def get_queryset(self, **kwargs):
        qs = super(BookCategoryListView, self).get_queryset()
        query = self.request.GET.get("q", None)
        if query is not None:
            qs = qs.filter(title__icontains=query)
        return qs


class BookCategoryDetailView(DetailView):
    model = BookCategory
    queryset = BookCategory.objects.all()
    template_name = 'books/book_category_detail.html'

    def get_context_data(self, **kwargs):
        context = super(BookCategoryDetailView, self).get_context_data(**kwargs)
        context.update({
            'main_category': BookMainCategory.objects.all(),
            'top_discount': BookDetail.objects.order_by('-discount').distinct()[:10],
            'blog_tags': BlogDetail.tags.all(),
            'book_tags': BookDetail.tags.all(),
            'course_tags': Course_detail.tags.all(),
            'recently_course_footer': Course_detail.objects.order_by('-id').filter(discount__range=(0, 99)).distinct()[
                                      :5],
            'discount_course_footer': Course_detail.objects.order_by('-discount').filter(
                discount__range=('1', '99')).distinct()[:5],
            'blog_footer': BlogDetail.objects.all().distinct()[:5],
        })
        obj = self.get_object()
        book_set = obj.bookdetail_set.order_by('-id').distinct()
        default_product = obj.default_category.order_by('-id').distinct()
        courses = (book_set | default_product)
        context['courses'] = courses
        return context

    def get_queryset(self, **kwargs):
        qs = super(BookCategoryDetailView, self).get_queryset()
        query = self.request.GET.get("q", None)
        if query is not None:
            qs = qs.filter(title__icontains=query)
        return qs


class CategoryTreeView(ListView):
    model = BookCategory
    template_name = 'myproject/category_tree.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryTreeView, self).get_context_data(**kwargs)
        context.update({
            'main_category': BookMainCategory.objects.all(),
            'course_all': BookDetail.objects.all(),
        })
        return context


class RecentlyUpdatedBookList(ListView):
    model = BookDetail
    template_name = 'books/recently_add_books_list.html'

    def get_context_data(self, **kwargs):
        context = super(RecentlyUpdatedBookList, self).get_context_data()
        context.update({
            'recently_updated': BookDetail.objects.order_by(str('-pk')).distinct(),
            'top_discount': BookDetail.objects.order_by('-discount').filter(discount__range=(0, 99)).distinct()[:8],
            'main_category': BookMainCategory.objects.all(),
            'blog_tags': BlogDetail.tags.all(),
            'book_tags': BookDetail.tags.all(),
            'course_tags': Course_detail.tags.all(),
            'recently_course_footer': Course_detail.objects.order_by('-id').filter(discount__range=(0, 99)).distinct()[
                                      :5],
            'discount_course_footer': Course_detail.objects.order_by('-discount').filter(
                discount__range=('1', '99')).distinct()[:5],
            'blog_footer': BlogDetail.objects.all().distinct()[:5],
        })
        return context

    def get_queryset(self, **kwargs):
        qs = super(RecentlyUpdatedBookList, self).get_queryset()
        query = self.request.GET.get("q", None)
        if query is not None:
            qs = qs.filter(title__icontains=query)
        return qs


class TopDiscountBookList(ListView):
    model = BookDetail
    template_name = 'books/top_discount_books_list.html'

    def get_context_data(self, **kwargs):
        context = super(TopDiscountBookList, self).get_context_data()
        context.update({
            'top_discount': BookDetail.objects.order_by('-discount').distinct(),
            'recently_updated': BookDetail.objects.order_by('-pk').filter(discount__range=(0, 99)).distinct()[:8],
            'main_category': BookMainCategory.objects.all(),
            'blog_tags': BlogDetail.tags.all(),
            'book_tags': BookDetail.tags.all(),
            'course_tags': Course_detail.tags.all(),
            'recently_course_footer': Course_detail.objects.order_by('-id').filter(discount__range=(0, 99)).distinct()[
                                      :5],
            'discount_course_footer': Course_detail.objects.order_by('-discount').filter(
                discount__range=('1', '99')).distinct()[:5],
            'blog_footer': BlogDetail.objects.all().distinct()[:5],
        })
        return context


class SearchDetailView(DetailView):
    model = BookCategory
    queryset = BookCategory.objects.all()
    template_name = 'search/search.html'

    def get_context_data(self, **kwargs):
        context = super(SearchDetailView, self).get_context_data(**kwargs)
        context.update({
            'main_category': BookMainCategory.objects.all(),
        })
        obj = self.get_object()
        course_set = obj.course_detail_set.all()
        default_product = obj.default_category.all()
        courses = (course_set | default_product)
        context['books'] = courses
        return context


def blog(request):
    return render(request, 'blog/blog.html', {})


class AllBook(ListView):
    model = BookDetail
    template_name = 'books/all_books.html'

    def get_context_data(self, **kwargs):
        context = super(AllBook, self).get_context_data()
        context.update({
            'all_courses': BookDetail.objects.order_by('-pk'),
            'recently_updated_books': BookDetail.objects.all(),
            'main_category': BookMainCategory.objects.all(),
            'category': BookCategory.objects.all(),
            'course_detail': Course_detail.objects.order_by('-id').distinct()[:10],
            'blog_tags': BlogDetail.tags.all(),
            'book_tags': BookDetail.tags.all(),
            'course_tags': Course_detail.tags.all(),
            'recently_course_footer': Course_detail.objects.order_by('-id').filter(discount__range=(0, 99)).distinct()[
                                      :5],
            'discount_course_footer': Course_detail.objects.order_by('-discount').filter(
                discount__range=('1', '99')).distinct()[:5],
            'blog_footer': BlogDetail.objects.all().distinct()[:5],
        })
        return context


def email(request):
    title = "Contact Us"
    form = ContactForm(request.POST or None)
    if form.is_valid():
        name = form.cleaned_data['name']
        subject = form.cleaned_data['subject']
        contact_email = form.cleaned_data['contact_email']
        message = form.cleaned_data['message']

        from_email = settings.EMAIL_HOST_USER
        to_email = [contact_email, from_email, ['vishal_22@hotmail.com']]

        contact_message = "{}: {}: {} via {}".format(
            name,
            subject,
            message,
            contact_email,
        )
        some_html_message = "<h3>Thank you for Your Feedback, We will get back to you withing 24 hrs.</h3><br><br>" \
                            "Name:<strong>{}</strong>,<br><br>" \
                            "Subject: <strong>{}</strong>,<br><br>" \
                            "Message: {} ,<br><br>" \
                            "via Email: <strong>{}</strong><br><br>".format(name, subject, message, contact_email)

        send_mail(name,
                  contact_message,
                  from_email,
                  to_email,
                  html_message=some_html_message,
                  )
    context = {
        "form": form,
        "title": title,
    }
    return render(request, "contact.html", context)


def success(request):
    return HttpResponse('Success! Thank you for your message.')
