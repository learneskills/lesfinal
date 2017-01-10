from haystack import indexes
from myproject.models import Course_detail, Category, MainCategory


class NoteIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    sub_title = indexes.CharField(model_attr='sub_title')
    description = indexes.CharField(model_attr='description')
    actual_price = indexes.IntegerField(model_attr='actual_price')
    sale_price = indexes.IntegerField(model_attr='sale_price')
    discount = indexes.IntegerField(model_attr='discount')
    review = indexes.BooleanField(model_attr='review')
    url = indexes.CharField(model_attr='url')
    course_provider = indexes.CharField(model_attr='course_provider')
    active = indexes.BooleanField(model_attr='active')

    def get_model(self):
        return Course_detail

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class CategoryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title2 = indexes.CharField(model_attr='title')
    timestamp = indexes.DateTimeField(model_attr='timestamp')

    def get_model(self):
        return Category

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class MainCategoryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title1 = indexes.CharField(model_attr='title')

    def get_model(self):
        return MainCategory

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
