from django.urls import path
from . import views

urlpatterns = [
    path('',                          views.home,           name='home'),
    path('posts/',                    views.approved_posts, name='approved-posts'),
    path('post/new/',                 views.create_post,    name='post-create'),
    path('post/<int:pk>/',            views.post_detail,    name='post-detail'),
    path('post/<int:pk>/edit/',       views.edit_post,      name='post-edit'),
    path('post/<int:pk>/delete/',     views.delete_post,    name='post-delete'),
    path('category/<slug:slug>/',     views.category_posts, name='category'),
    path('editor/',                   views.editor_panel,   name='editor-panel'),
    path('editor/approve/<int:pk>/',  views.approve_post,   name='approve-post'),
    path('editor/reject/<int:pk>/',   views.reject_post,    name='reject-post'),
]
