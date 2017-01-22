from haystack import indexes
from myproject.models import Course_detail, Category, MainCategory


class NoteIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    course_title = indexes.CharField(model_attr='title')
    course_sub_title = indexes.CharField(model_attr='sub_title')
    course_description = indexes.CharField(model_attr='description')
    course_actual_price = indexes.IntegerField(model_attr='actual_price')
    course_sale_price = indexes.IntegerField(model_attr='sale_price')
    course_discount = indexes.IntegerField(model_attr='discount')
    course_review = indexes.BooleanField(model_attr='review')
    course_url = indexes.CharField(model_attr='url')
    course_course_provider = indexes.CharField(model_attr='course_provider')
    course_student_enrolled = indexes.IntegerField(model_attr='student_enrolled')
    course_active = indexes.BooleanField(model_attr='active')

    def get_model(self):
        return Course_detail

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class CategoryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    course_category_title = indexes.CharField(model_attr='title')
    course_category_timestamp = indexes.DateTimeField(model_attr='timestamp')

    def get_model(self):
        return Category

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class MainCategoryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    course_main_category_title = indexes.CharField(model_attr='title')

    def get_model(self):
        return MainCategory

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
