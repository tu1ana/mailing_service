from django.urls import path

from blog.apps import BlogConfig
from blog.views import BlogListView, BlogCreateView, BlogDetailView

app_name = BlogConfig.name

urlpatterns = [
    path('list/', BlogListView.as_view(), name='blog_list'),
    path('create/', BlogCreateView.as_view(), name='blog_create'),
    path('view/<int:pk>', BlogDetailView.as_view(), name='blog_view'),
]
