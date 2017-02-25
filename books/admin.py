from django.contrib import admin
from .models import BookMainCategory, BookCategory, BookCategoryImage, BookDetail, BookImage
from tinymce.widgets import TinyMCE
from books import models
# Register your models here.


class BookDetailModelAdmin(admin.ModelAdmin):
    date_hierarchy = 'pub_date'
    list_display = ('title', 'default', 'discount', 'sale_price', 'pub_date')
    list_filter = ('discount', 'categories')
    search_fields = ['title']
    formfield_overrides = {
        models.tinymce_models.HTMLField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},
    }

admin.site.register(BookDetail, BookDetailModelAdmin)


class BookImageModelAdmin(admin.ModelAdmin):
    actions_on_top = True

admin.site.register(BookImage, BookImageModelAdmin)

admin.site.register(BookMainCategory)
admin.site.register(BookCategory)
admin.site.register(BookCategoryImage)

