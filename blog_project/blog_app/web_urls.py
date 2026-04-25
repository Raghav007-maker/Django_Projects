from django.urls import path
from .views import (
    home_view,
    post_detail_view,
    login_view,
    signup_view,
    create_post_view,
    edit_post_view,
    delete_post_view,
    toggle_like_view,
    add_comment_view,
    logout_view,
)

urlpatterns = [
    path('', home_view, name='home'),
    path('post/<int:post_id>/', post_detail_view, name='post_detail'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('create-post/', create_post_view, name='create_post'),
    path('post/<int:post_id>/edit/', edit_post_view, name='edit_post'),
    path('post/<int:post_id>/delete/', delete_post_view, name='delete_post'),
    path('post/<int:post_id>/like/', toggle_like_view, name='toggle_like'),
    path('post/<int:post_id>/comment/', add_comment_view, name='add_comment'),
    path('logout/', logout_view, name='logout'),
]
