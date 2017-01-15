from haystack import indexes
from myproject.models import Course_detail, Category, MainCategory
from books.models import BookDetail, BookCategory, BookMainCategory


class NoteIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    author_name = indexes.CharField(model_attr='author_name')
    description = indexes.CharField(model_attr='description')
    actual_price = indexes.IntegerField(model_attr='actual_price')
    sale_price = indexes.IntegerField(model_attr='sale_price')
    discount = indexes.IntegerField(model_attr='discount')
    rating = indexes.BooleanField(model_attr='rating')
    url = indexes.CharField(model_attr='url')
    paperback = indexes.IntegerField(model_attr='paperback')
    active = indexes.BooleanField(model_attr='active')

    def get_model(self):
        return BookDetail

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class CategoryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title2 = indexes.CharField(model_attr='title')
    timestamp = indexes.DateTimeField(model_attr='timestamp')

    def get_model(self):
        return BookCategory

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class MainCategoryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title1 = indexes.CharField(model_attr='title')

    def get_model(self):
        return BookMainCategory

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
