from django.core.urlresolvers import reverse
from django.db import models

# Create your models here.
from django.utils.text import slugify
from taggit.managers import TaggableManager
from tinymce import models as tinymce_models


class CourseQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)


# Manager Model
class CourseManager(models.Manager):
    def get_queryset(self):
        return CourseQuerySet(self.model, using=self._db)

    def all(self, *args, **kwargs):
        return self.get_queryset().active()

    def get_related(self, instance):
        course_one = self.get_queryset().filter(categories__in=instance.categories.all())
        course_two = self.get_queryset().filter(default=instance.default)
        qs = (course_one | course_two).exclude(id=instance.id).distinct()

        return qs


# Course Details

class MainCategory(models.Model):
    title = models.CharField(max_length=30)
    slug = models.SlugField()

    def __str__(self):
        return self.title


class Category(models.Model):
    category = models.ForeignKey(MainCategory)
    title = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(unique=True)
    default = models.ForeignKey('MainCategory', related_name='default_main_category', null=True, blank=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})

    def get_image_url(self):
        cat_img = self.categoryimage_set.first()
        if cat_img:
            return cat_img.image.url
        return cat_img

    class Meta:
        ordering = ["-title"]


class CourseProvider(models.Model):
    course_provider_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)

    def __str__(self):
        return self.course_provider_name

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)
        super(CourseProvider, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("provider", kwargs={"slug": self.slug})


class Course_detail(models.Model):
    Main_Category = models.ForeignKey('MainCategory', blank=True)
    categories = models.ManyToManyField('Category', blank=True)
    default = models.ForeignKey('Category', related_name='default_category', null=True, blank=True)
    course_provider = models.ForeignKey(CourseProvider, blank=True, null=True)
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(null=True, blank=True, max_length=50)
    sub_title = models.CharField(max_length=200)
    description = tinymce_models.HTMLField(null=True)
    actual_price = models.DecimalField(null=True, decimal_places=2, max_digits=6)
    sale_price = models.DecimalField(null=True, decimal_places=2, max_digits=6)
    discount = models.PositiveIntegerField(null=True)
    review = models.BooleanField(default=True)
    url = models.URLField(blank=True, max_length=200)
    pub_date = models.DateTimeField(auto_now=True, auto_now_add=False)
    updated_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    student_enrolled = models.PositiveIntegerField(null=True)
    active = models.BooleanField(default=True)

    objects = CourseManager()
    tags = TaggableManager()

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)
        super(Course_detail, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-title"]

    def get_absolute_url(self):
        return reverse("single-product", kwargs={"slug": self.slug, "pk": self.pk})

    def get_image_url(self):
        img = self.courseimage_set.first()
        if img:
            return img.image.url
        return img

    def get_tag_url(self):
        return reverse("tagged", kwargs={"slug": self.slug})


# Course Images
class CourseImage(models.Model):
    course = models.ForeignKey(Course_detail)
    image = models.ImageField(upload_to='media_root/')
    image_height = models.PositiveIntegerField(null=True, blank=True, editable=False, default="100")
    image_width = models.PositiveIntegerField(null=True, blank=True, editable=False, default="100")

    def __str__(self):
        return self.course.title


class CategoryImage(models.Model):
    category_image = models.ForeignKey(Category)
    image = models.ImageField(upload_to='media_root/')
    image_height = models.PositiveIntegerField(null=True, blank=True, editable=False, default="100")
    image_width = models.PositiveIntegerField(null=True, blank=True, editable=False, default="100")

    def __str__(self):
        return self.category_image.title


from django.utils.translation import ugettext_lazy as _

from newsletter_subscription.models import SubscriptionBase


class Subscription(SubscriptionBase):
    full_name = models.CharField(_('full name'), max_length=100, blank=True)
