from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE
from myproject import models
from .models import Category, Course_detail, CourseImage, MainCategory, CategoryImage, CourseProvider


# Register your models here.

class CourseDetailModelAdmin(admin.ModelAdmin):
    date_hierarchy = 'pub_date'
    list_display = ('title', 'default', 'course_provider', 'discount', 'sale_price', 'pub_date')
    list_filter = ('course_provider', 'discount', 'categories')
    search_fields = ['title']
    formfield_overrides = {
        models.tinymce_models.HTMLField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},
    }


class CourseImageModelAdmin(admin.ModelAdmin):
    actions_on_top = True
admin.site.register(CourseImage, CourseImageModelAdmin)



admin.site.register(Course_detail, CourseDetailModelAdmin)
admin.site.register(MainCategory)
admin.site.register(Category)
admin.site.register(CategoryImage)
admin.site.register(CourseProvider)
