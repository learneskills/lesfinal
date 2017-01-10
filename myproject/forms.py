from django import forms
from myproject.models import Course_detail, CourseImage
from haystack.forms import SearchForm


class CourseModelForm(forms.ModelForm):
    class Meta:
        model = Course_detail
        fields = [
            'Main_Category',
            'categories',
            'default',
            'title',
            'slug',
            'sub_title',
            'description',
            'actual_price',
            'sale_price',
            'discount',
            'review',
            'url',
            'course_provider',
            'active',
        ]

        # def clean_title(self):
        #     title = self.cleaned_data("title")
        #     return title


class CourseModelImage(forms.ModelForm):
    class Meta:
        model = CourseImage
        fields = ['course', 'image']


class ContactForm(forms.Form):
    name = forms.CharField(required=True)
    contact_email = forms.CharField(required=True)
    subject = forms.CharField(required=True, max_length=200)
    message = forms.CharField(widget=forms.Textarea)
