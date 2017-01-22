from haystack import indexes
from myproject.models import Course_detail, Category, MainCategory
from books.models import BookDetail, BookCategory, BookMainCategory


class NoteIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    book_title = indexes.CharField(model_attr='title')
    book_author_name = indexes.CharField(model_attr='author_name')
    book_description = indexes.CharField(model_attr='description')
    book_actual_price = indexes.IntegerField(model_attr='actual_price')
    book_sale_price = indexes.IntegerField(model_attr='sale_price')
    book_discount = indexes.IntegerField(model_attr='discount')
    book_rating = indexes.BooleanField(model_attr='rating')
    book_url = indexes.CharField(model_attr='url')
    book_paperback = indexes.IntegerField(model_attr='paperback')
    book_active = indexes.BooleanField(model_attr='active')

    def get_model(self):
        return BookDetail

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class CategoryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    book_category_title = indexes.CharField(model_attr='title')
    book_category_timestamp = indexes.DateTimeField(model_attr='timestamp')

    def get_model(self):
        return BookCategory

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class MainCategoryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    book_main_category_title = indexes.CharField(model_attr='title')

    def get_model(self):
        return BookMainCategory

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
