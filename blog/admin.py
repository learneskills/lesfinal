from django.contrib import admin
from tinymce.widgets import TinyMCE

from books import models
from .models import BlogDetail, BlogCategory, BlogMainCategory, PostBy, BlogImage

# Register your models here.


class BlogDetailModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.tinymce_models.HTMLField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},
    }

admin.site.register(BlogDetail, BlogDetailModelAdmin)
admin.site.register(BlogCategory)
admin.site.register(BlogMainCategory)
admin.site.register(PostBy)
admin.site.register(BlogImage)
