from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home_page"),
    path('signin/', views.signin, name="sigin_page"),
    path('signup/', views.signup, name="sigup_page"),
]
