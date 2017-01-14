from django.core.urlresolvers import reverse
from django.db import models

# Create your models here.
from django.utils.text import slugify
from taggit.managers import TaggableManager
from tinymce import models as tinymce_models


class BookQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)


# Manager Model
class BookManager(models.Manager):
    def get_queryset(self):
        return BookQuerySet(self.model, using=self._db)

    def all(self, *args, **kwargs):
        return self.get_queryset().active()

    def get_related(self, instance):
        course_one = self.get_queryset().filter(categories__in=instance.categories.all())
        course_two = self.get_queryset().filter(default=instance.default)
        qs = (course_one | course_two).exclude(id=instance.id).distinct()

        return qs


# Course Details

class BookMainCategory(models.Model):
    title = models.CharField(max_length=30)
    slug = models.SlugField()

    def __str__(self):
        return self.title


class BookCategory(models.Model):
    category = models.ForeignKey(BookMainCategory)
    title = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(unique=True)
    default = models.ForeignKey('BookMainCategory', related_name='default_main_category', null=True, blank=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book_category_detail", kwargs={"slug": self.slug})

    def get_image_url(self):
        cat_img = self.categoryimage_set.first()
        if cat_img:
            return cat_img.image.url
        return cat_img


class BookDetail(models.Model):
    Main_Category = models.ForeignKey('BookMainCategory', blank=True)
    categories = models.ManyToManyField('BookCategory', blank=True)
    default = models.ForeignKey('BookCategory', related_name='default_category', null=True, blank=True)
    title = models.CharField(max_length=200, unique=True)
    author_name = models.CharField(max_length=100)
    slug = models.SlugField(null=True, blank=True)
    actual_price = models.DecimalField(null=True, decimal_places=2, max_digits=6)
    sale_price = models.DecimalField(null=True, decimal_places=2, max_digits=6)
    description = tinymce_models.HTMLField(null=True)
    discount = models.PositiveIntegerField(null=True)
    rating = models.BooleanField(default=True)
    url = models.URLField(blank=True, max_length=200)
    paperback = models.IntegerField(null=True)
    active = models.BooleanField(default=True)

    objects = BookManager()
    tags = TaggableManager()

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)
        super(BookDetail, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-title"]

    def get_absolute_url(self):
        return reverse("single-book-detail", kwargs={"slug": self.slug})

    def get_image_url(self):
        img = self.courseimage_set.first()
        if img:
            return img.image.url
        return img

    def get_tag_url(self):
        return reverse("book-tagged", kwargs={"slug": self.slug})


# Course Images
class BookImage(models.Model):
    course = models.ForeignKey(BookDetail)
    image = models.ImageField(upload_to='media_root/books/')
    image_height = models.PositiveIntegerField(null=True, blank=True, editable=False, default="100")
    image_width = models.PositiveIntegerField(null=True, blank=True, editable=False, default="100")

    def __str__(self):
        return self.course.title


class BookCategoryImage(models.Model):
    category_image = models.ForeignKey(BookCategory)
    image = models.ImageField(upload_to='media_root/books/')
    image_height = models.PositiveIntegerField(null=True, blank=True, editable=False, default="100")
    image_width = models.PositiveIntegerField(null=True, blank=True, editable=False, default="100")

    def __str__(self):
        return self.category_image.title
