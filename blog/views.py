from django.views.generic import DetailView
from django.views.generic.list import ListView
from taggit.models import Tag

from .models import BlogDetail, BlogCategory, BlogMainCategory


# Create your views here.

class TagMixin(object):
    def get_context_data(self, **kwargs):
        context = super(TagMixin, self).get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        return context


class BlogList(ListView):
    model = BlogDetail
    template_name = 'blog.html'

    def get_context_data(self, **kwargs):
        context = super(BlogList, self).get_context_data(**kwargs)
        context.update({
            'blog_category': BlogCategory.objects.all(),
            'blog_maincategory': BlogMainCategory.objects.all(),
            'blog_list_content': BlogDetail.objects.order_by('-id'),
            'recent_post': BlogDetail.objects.order_by('-id').distinct()[:5],
            'all_tags': BlogDetail.tags.all(),
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
            'recent_post': BlogDetail.objects.order_by('-id').distinct()[:5],
            'all_tags': BlogDetail.tags.all(),
        })
        return context


class TagIndexView(TagMixin, ListView):
    model = BlogDetail
    queryset = BlogDetail.objects.all()
    template_name = 'blog/tag_detail.html'

    def get_queryset(self):
        return BlogDetail.objects.filter(tags__slug=self.kwargs.get('slug'))

    def get_context_data(self, **kwargs):
        context = super(TagIndexView, self).get_context_data(**kwargs)
        context.update({
            'main_category': BlogMainCategory.objects.all(),
            'blog_category': BlogCategory.objects.all(),
            'recent_post': BlogDetail.objects.order_by('-id').distinct()[:5],
            'all_blog': BlogDetail.objects.all(),
            'all_tags': BlogDetail.tags.all(),

        })
        return context
