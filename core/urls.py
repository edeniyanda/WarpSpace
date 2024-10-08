from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name="home_page"),
    path('signin/', views.signin, name="signin_page"),
    path('signup/', views.signup, name="signup_page"),
    path('logout/', LogoutView.as_view(template_name='core/logout.html'), name='logout_page'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('profile/<str:username>/followers/', views.followers_list, name='followers_list'),
    path('profile/<str:username>/following/', views.following_list, name='followings_list'),
    path('settings/', views.edit_profile, name='edit_profile'),
    path('feeds/', views.feeds, name='feeds_page'),
    path('post/', views.create_post, name='create_post'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('repost/<int:post_id>/', views.repost_post, name='repost_post'),
    path('follow/<str:username>/', views.follow_unfollow, name='follow_unfollow'),
    path('search/', views.search, name='search_page'),
]
