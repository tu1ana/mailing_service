from django import forms

from blog.models import Blog
from mailout.forms import StyleFormMixin


class BlogForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Blog
        exclude = ('author', 'views_count')
