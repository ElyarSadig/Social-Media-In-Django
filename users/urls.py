from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),

    path('user-settings/', views.settings, name='settings'),
    path('reset-password/', views.change_password, name='change-password'),

    path("user-profile/", views.user_profile, name="user-profile"),
    path("profile-view/<str:pk>/", views.profile_view, name="profile-view"),
]