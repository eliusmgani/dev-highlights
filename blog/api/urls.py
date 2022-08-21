from django.urls import path
from blog.api.views import (
    api_detail_blog_view,
    api_update_blog_view,
    api_delete_blog_view,
    api_create_blog_view,
    ApiBlogListView,
    api_is_author_of_blogpost,
)

app_name = 'blog'

urlpatterns = [
    path('<slug>/', api_detail_blog_view, name="Detail"),
    path('<slug>/update', api_update_blog_view, name="Update"),
    path('<slug>/dalete', api_delete_blog_view, name="Delete"),
    path('create', api_create_blog_view, name="Create"),
    path('list', ApiBlogListView.as_view(), name="List"),
    path('<slug>/is_author', api_is_author_of_blogpost, name="is_author"),
]