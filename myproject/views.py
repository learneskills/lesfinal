import random

from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.list import ListView
from taggit.models import Tag

from myproject.forms import ContactForm
from myproject.models import Category, MainCategory
from webproject import settings
from .forms import CourseModelForm, CourseModelImage
from .models import Course_detail, CourseProvider
from books.models import BookMainCategory, BookCategory, BookDetail
from blog.models import BlogDetail, BlogCategory, BlogMainCategory
from hitcount.views import HitCountDetailView, HitCountMixin


class TagMixin(object):
    def get_context_data(self, **kwargs):
        context = super(TagMixin, self).get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        return context


class SingleProductDetailView(TagMixin, HitCountDetailView):
    model = Course_detail
    count_hit = True
    queryset = Course_detail.objects.all()
    template_name = 'myproject/single_product.html'

    def get_context_data(self, **kwargs):
        context = super(SingleProductDetailView, self).get_context_data(**kwargs)
        context.update({
            'main_category': MainCategory.objects.all(),
            'recently_updated': Course_detail.objects.order_by('-id').distinct()[:10],
            'top_discount': Course_detail.objects.order_by('-discount').filter(discount__range=(0, 99)).distinct()[:10],
            'blog_tags': BlogDetail.tags.all(),
            'book_tags': BookDetail.tags.all(),
            'course_tags': Course_detail.tags.all(),
            'recently_book_footer': BookDetail.objects.order_by('-id').filter(discount__range=(0, 99)).distinct()[:5],
            'discount_book_footer': BookDetail.objects.order_by('-discount').filter(
                discount__range=('1', '99')).distinct()[:5],
            'blog_footer': BlogDetail.objects.all().distinct()[:5],

        })
        instance = self.get_object()
        context["related"] = sorted(Course_detail.objects.get_related(instance).distinct()[:10],
                                    key=lambda x: random.random())
        return context


class TagIndexView(TagMixin, ListView):
    model = Course_detail
    queryset = Course_detail.objects.all()
    template_name = 'myproject/tag_detail.html'

    def get_queryset(self):
        return Course_detail.objects.filter(tags__slug=self.kwargs.get('slug'))

    def get_context_data(self, **kwargs):
        context = super(TagIndexView, self).get_context_data(**kwargs)
        context.update({
            'main_category': MainCategory.objects.all(),
            'category': Category.objects.all(),
            'recently_updated': Course_detail.objects.order_by('-id').distinct()[:3],
            'top_discount': Course_detail.objects.order_by('-discount').distinct()[:3],
            'blog_tags': BlogDetail.tags.all(),
            'book_tags': BookDetail.tags.all(),
            'course_tags': Course_detail.tags.all(),
            'recently_book_footer': BookDetail.objects.order_by('-id').filter(discount__range=(0, 99)).distinct()[:5],
            'discount_book_footer': BookDetail.objects.order_by('-discount').filter(
                discount__range=('1', '99')).distinct()[:5],
            'blog_footer': BlogDetail.objects.all().distinct()[:5],
        })
        return context


class CategoryListView(HitCountMixin, ListView):
    model = Category
    count_hit = True
    paginate_by = 4
    template_name = 'index.html'
    context_object_name = 'category_list'

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)

        context.update({
            'course_detail_discount_list': Course_detail.objects.order_by('-discount').filter(
                discount__range=('10', '99')).distinct()[:8],
            'course_detail_recently_updated_list': Course_detail.objects.order_by('-pk').distinct()[:8],
            'course_all': Course_detail.objects.order_by('-title'),
            'main_category': MainCategory.objects.order_by('id'),
            'book_main_category': BookMainCategory.objects.all(),
            'book_category': BookCategory.objects.all(),
            'book_all': BookDetail.objects.order_by('-title'),
            'top_discount_book': BookDetail.objects.order_by('-discount').filter(
                discount__range=('0', '99')).distinct()[:8],
            'recently_updated_book': BookDetail.objects.order_by('-id').distinct()[:8],
            'course_provider_list': CourseProvider.objects.all(),
            'blog_tags': BlogDetail.tags.all(),
            'book_tags': BookDetail.tags.all(),
            'course_tags': Course_detail.tags.all(),
            'course_footer': Course_detail.objects.all().order_by('-student_enrolled').filter(
                student_enrolled__range=(20000, 200000)).filter(discount__range=(1, 99)).distinct()[:5],
            'book_footer': BookDetail.objects.all().filter(discount__range=(5, 99)).distinct()[:5],
            'blog_footer': BlogDetail.objects.all().distinct()[:5],
        })
        return context

    def get_queryset(self, **kwargs):
        qs = super(CategoryListView, self).get_queryset()
        query = self.request.GET.get("q", None)
        if query is not None:
            qs = qs.filter(title__icontains=query)
        return qs


class CategoryDetailView(DetailView):
    model = Category
    queryset = Category.objects.all()
    template_name = 'myproject/category_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        context.update({
            'main_category': MainCategory.objects.all(),
            'top_discount': Course_detail.objects.order_by('-discount').filter(discount__range=(1, 99)).distinct()[:10],
            'blog_tags': BlogDetail.tags.all(),
            'book_tags': BookDetail.tags.all(),
            'course_tags': Course_detail.tags.all(),
            'recently_book_footer': BookDetail.objects.order_by('-id').filter(discount__range=(0, 99)).distinct()[:5],
            'discount_book_footer': BookDetail.objects.order_by('-discount').filter(
                discount__range=('1', '99')).distinct()[:5],
            'blog_footer': BlogDetail.objects.all().distinct()[:5],
        })
        obj = self.get_object()
        course_set = obj.course_detail_set.order_by('-id').distinct()
        default_product = obj.default_category.order_by('-id').distinct()
        courses = (course_set | default_product)
        context['courses'] = courses

        return context

    def get_queryset(self, **kwargs):
        qs = super(CategoryDetailView, self).get_queryset()
        query = self.request.GET.get("q", None)
        if query is not None:
            qs = qs.filter(title__icontains=query)
        return qs


class CategoryTreeView(ListView):
    model = Category
    template_name = 'myproject/category_tree.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryTreeView, self).get_context_data(**kwargs)
        context.update({
            'main_category': MainCategory.objects.all(),
            'course_all': Course_detail.objects.all(),
        })
        return context


class RecentlyUpdatedList(ListView):
    model = Course_detail
    template_name = 'myproject/recently_add_list.html'

    def get_context_data(self, **kwargs):
        context = super(RecentlyUpdatedList, self).get_context_data()
        context.update({
            'recently_updated': Course_detail.objects.order_by(str('-pk')).distinct(),
            'top_discount': Course_detail.objects.order_by('-discount').filter(discount__range=(0, 99)).distinct()[:8],
            'main_category': MainCategory.objects.all(),
            'blog_tags': BlogDetail.tags.all(),
            'book_tags': BookDetail.tags.all(),
            'course_tags': Course_detail.tags.all(),
            'recently_book_footer': BookDetail.objects.order_by('-id').filter(discount__range=(0, 99)).distinct()[:5],
            'discount_book_footer': BookDetail.objects.order_by('-discount').filter(
                discount__range=('1', '99')).distinct()[:5],
            'blog_footer': BlogDetail.objects.all().distinct()[:5],
        })
        return context

    def get_queryset(self, **kwargs):
        qs = super(RecentlyUpdatedList, self).get_queryset()
        query = self.request.GET.get("q", None)
        if query is not None:
            qs = qs.filter(title__icontains=query)
        return qs


class TopDiscountList(ListView):
    model = Course_detail
    template_name = 'myproject/top_discount_list.html'

    def get_context_data(self, **kwargs):
        context = super(TopDiscountList, self).get_context_data()
        context.update({
            'top_discount': Course_detail.objects.order_by('-discount').distinct(),
            'recently_updated': Course_detail.objects.order_by('-pk').distinct()[:8],
            'main_category': MainCategory.objects.all(),
            'blog_tags': BlogDetail.tags.all(),
            'book_tags': BookDetail.tags.all(),
            'course_tags': Course_detail.tags.all(),
            'recently_book_footer': BookDetail.objects.order_by('-id').filter(discount__range=(0, 99)).distinct()[:5],
            'discount_book_footer': BookDetail.objects.order_by('-discount').filter(
                discount__range=('1', '99')).distinct()[:5],
            'blog_footer': BlogDetail.objects.all().distinct()[:5],
        })
        return context


@login_required
def course_model_form(request):
    title = "Course Detail Form"
    form = CourseModelForm(request.POST or None)
    if form.is_valid():
        form.save()

    return render(request, 'form.html', {"title": title, "form": form})


@login_required
def image_model_form(request):
    title = "Upload Images"
    form = CourseModelImage(request.POST or None)
    if form.is_valid():
        form.save()

    return render(request, 'img_form.html', {"title": title, "form": form})


class AllCourse(ListView):
    model = Course_detail
    template_name = 'myproject/all_course.html'

    def get_context_data(self, **kwargs):
        context = super(AllCourse, self).get_context_data()
        context.update({
            'all_courses': Course_detail.objects.order_by('-pk'),
            'recently_updated': Course_detail.objects.all(),
            'main_category': MainCategory.objects.all(),
            'category': Category.objects.all(),
            'book_detail': BookDetail.objects.order_by('-id').distinct()[:10],
            'blog_tags': BlogDetail.tags.all(),
            'book_tags': BookDetail.tags.all(),
            'course_tags': Course_detail.tags.all(),
            'recently_book_footer': BookDetail.objects.order_by('-id').filter(discount__range=(0, 99)).distinct()[:5],
            'discount_book_footer': BookDetail.objects.order_by('-discount').filter(
                discount__range=('1', '99')).distinct()[:5],
            'blog_footer': BlogDetail.objects.all().distinct()[:5],
        })
        return context


class CourseProviderStore(DetailView):
    model = CourseProvider
    template_name = 'myproject/course_provider_store.html'

    def get_context_data(self, **kwargs):
        context = super(CourseProviderStore, self).get_context_data()
        context.update({
            'blog_tags': BlogDetail.tags.all(),
            'book_tags': BookDetail.tags.all(),
            'course_tags': Course_detail.tags.all(),
            'recently_book_footer': BookDetail.objects.order_by('-id').filter(discount__range=(0, 99)).distinct()[:5],
            'discount_book_footer': BookDetail.objects.order_by('-discount').filter(
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
        'blog_tags': BlogDetail.tags.all(),
        'book_tags': BookDetail.tags.all(),
        'course_tags': Course_detail.tags.all(),
        'recently_course_footer': Course_detail.objects.order_by('-id').filter(discount__range=(0, 99)).distinct()[
                                  :5],
        'discount_course_footer': Course_detail.objects.order_by('-discount').filter(
            discount__range=('1', '99')).distinct()[:5],
        'blog_footer': BlogDetail.objects.all().distinct()[:5],

    }
    return render(request, "contact.html", context)


def success(request):
    return HttpResponse('Success! Thank you for your message.')
