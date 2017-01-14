from django.contrib import admin
from .models import BookMainCategory, BookCategory, BookCategoryImage, BookDetail, BookImage

# Register your models here.

admin.site.register(BookMainCategory)
admin.site.register(BookCategory)
admin.site.register(BookCategoryImage)
admin.site.register(BookDetail)
admin.site.register(BookImage)
