from django.contrib import admin
from django.db import models
from tinymce.models import HTMLField
from tinymce.widgets import TinyMCE

from myproject import models
from .models import Category, Course_detail, CourseImage, MainCategory, CategoryImage


# Register your models here.


class CourseDetailModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.tinymce_models.HTMLField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},
    }


admin.site.register(Course_detail, CourseDetailModelAdmin)
admin.site.register(CourseImage)
admin.site.register(MainCategory)
admin.site.register(Category)
admin.site.register(CategoryImage)
