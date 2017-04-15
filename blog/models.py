# Create your models here.
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.text import slugify
from taggit.managers import TaggableManager
from tinymce import models as tinymce_models


class BlogQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)


# Manager Model
class BlogManager(models.Manager):
    def get_queryset(self):
        return BlogQuerySet(self.model, using=self._db)

    def all(self, *args, **kwargs):
        return self.get_queryset().active()

    def get_related(self, instance):
        course_one = self.get_queryset().filter(categories__in=instance.categories.all())
        course_two = self.get_queryset().filter(default=instance.default)
        qs = (course_one | course_two).exclude(id=instance.id).distinct()

        return qs


# Course Details

class BlogMainCategory(models.Model):
    title = models.CharField(max_length=30)
    slug = models.SlugField()

    def __str__(self):
        return self.title


class BlogCategory(models.Model):
    category = models.ForeignKey(BlogMainCategory)
    title = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(unique=True)
    default = models.ForeignKey('BlogMainCategory', related_name='default_main_category', null=True, blank=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog_category_detail_view", kwargs={"slug": self.slug})

    def get_image_url(self):
        cat_img = self.categoryimage_set.first()
        if cat_img:
            return cat_img.image.url
        return cat_img


class PostBy(models.Model):
    posted_by = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.posted_by

    def save(self, *args, **kwargs):
        if not self.slug and self.posted_by:
            self.slug = slugify(self.posted_by)
        super(PostBy, self).save(*args, **kwargs)


class BlogDetail(models.Model):
    Main_Category = models.ForeignKey('BlogMainCategory', blank=True)
    categories = models.ManyToManyField('BlogCategory', blank=True)
    default = models.ForeignKey('BlogCategory', related_name='default_category', null=True, blank=True)
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(null=True, blank=True, max_length=50)
    description = tinymce_models.HTMLField(null=True)
    post_by = models.ForeignKey(PostBy, blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    update = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)

    objects = BlogManager()
    tags = TaggableManager()

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)
        super(BlogDetail, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-title"]

    def get_absolute_url(self):
        return reverse("blog-detail", kwargs={"slug": self.slug})

    def get_image_url(self):
        img = self.courseimage_set.first()
        if img:
            return img.image.url
        return img

    def get_tag_url(self):
        return reverse("blog_tagged", kwargs={"slug": self.slug})


# Course Images
class BlogImage(models.Model):
    course = models.ForeignKey(BlogDetail)
    image = models.ImageField(upload_to='media_root/blog/')
    image_height = models.PositiveIntegerField(null=True, blank=True, editable=False, default="100")
    image_width = models.PositiveIntegerField(null=True, blank=True, editable=False, default="100")

    def __str__(self):
        return self.course.title


class BlogCategoryImage(models.Model):
    category_image = models.ForeignKey(BlogCategory)
    image = models.ImageField(upload_to='media_root/blog/')
    image_height = models.PositiveIntegerField(null=True, blank=True, editable=False, default="100")
    image_width = models.PositiveIntegerField(null=True, blank=True, editable=False, default="100")

    def __str__(self):
        return self.category_image.title
