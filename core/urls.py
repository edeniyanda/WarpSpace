from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name="home_page"),
    path('signin/', views.signin, name="signin_page"),
    path('signup/', views.signup, name="signup_page"),
    path('logout/', LogoutView.as_view(template_name='core/logout.html'), name='logout_page'),
    path('profile/<str:username>/', views.profile_view, name='profile'),

]
