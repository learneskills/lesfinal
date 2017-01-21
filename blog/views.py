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
    template_name = 'blog/blog.html'

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
    template_name = 'blog/blog-post.html'

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


class BlogCategoryDetailView(DetailView):
    model = BlogCategory
    queryset = BlogCategory.objects.all()
    template_name = 'blog/blog_category.html'

    def get_context_data(self, **kwargs):
        context = super(BlogCategoryDetailView, self).get_context_data(**kwargs)
        context.update({
            'main_category': BlogMainCategory.objects.all(),
            'top_discount': BlogDetail.objects.order_by('-discount').distinct()[:10],
            'blog_category': BlogCategory.objects.all(),
            'blog_maincategory': BlogMainCategory.objects.all(),
            'blog_list_content': BlogDetail.objects.order_by('-id'),
            'recent_post': BlogDetail.objects.order_by('-id').distinct()[:5],
            'all_tags': BlogDetail.tags.all(),
        })
        obj = self.get_object()
        blog_set = obj.blogdetail_set.all()
        default_blog = obj.default_category.all()
        blogs = (blog_set | default_blog)
        context['blogs'] = blogs
        return context

    def get_queryset(self, **kwargs):
        qs = super(BlogCategoryDetailView, self).get_queryset()
        query = self.request.GET.get("q", None)
        if query is not None:
            qs = qs.filter(title__icontains=query)
        return qs