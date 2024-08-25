from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home_page"),
    path('signin/', views.signin, name="signin_page"),
    path('signup/', views.signup, name="signup_page"),
]
