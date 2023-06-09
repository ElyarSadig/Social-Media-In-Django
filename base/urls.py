from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),

    path("like-post/<str:pk>/", views.like_post, name="like"),
    path("create-post/", views.create_post, name='create-post'),
    path("update-post/<str:pk>/", views.update_post, name='update-post'),
    path("delete-post/<str:pk>/", views.delete_post, name="delete-post"),

    path("follow_user/<str:pk>/", views.follow_user, name="follow_user"),
    path("user-posts/", views.user_posts, name="user-posts"),

    path("comments/<str:pk>/", views.comments, name="comments"),
]