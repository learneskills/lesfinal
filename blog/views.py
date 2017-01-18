from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.list import ListView
from .models import BlogDetail, BlogCategory, BlogMainCategory


# Create your views here.


class BlogList(ListView):
    model = BlogDetail
    queryset = BlogDetail.objects.all()
    template_name = 'blog.html'

    def get_context_data(self, **kwargs):
        context = super(BlogList, self).get_context_data(**kwargs)
        context.update({
            'blog_category': BlogCategory.objects.all(),
            'blog_maincategory': BlogMainCategory.objects.all(),
        })
        return context


class BlogDetailView(DetailView):
    model = BlogDetail
    queryset = BlogDetail.objects.all()
    template_name = 'blog-post.html'

    def get_context_data(self, **kwargs):
        context = super(BlogDetailView, self).get_context_data(**kwargs)
        context.update({
            'blog_category': BlogCategory.objects.all(),
            'blog_maincategory': BlogMainCategory.objects.all(),
            'recent_post': BlogDetail.objects.order_by('-id'),
        })
        return context
