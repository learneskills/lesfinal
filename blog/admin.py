from django.contrib import admin
from tinymce.widgets import TinyMCE

from books import models
from .models import BlogDetail, BlogCategory, BlogMainCategory, PostBy, BlogImage

# Register your models here.


class BlogDetailModelAdmin(admin.ModelAdmin):
    date_hierarchy = 'timestamp'
    list_display = ('title', 'default', 'post_by', 'timestamp')
    list_filter = ('default', 'update')
    search_fields = ['title']
    formfield_overrides = {
        models.tinymce_models.HTMLField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},
    }

admin.site.register(BlogDetail, BlogDetailModelAdmin)


class BlogImageModelAdmin(admin.ModelAdmin):
    actions_on_top = True
admin.site.register(BlogImage, BlogImageModelAdmin)

admin.site.register(BlogCategory)
admin.site.register(BlogMainCategory)
admin.site.register(PostBy)

