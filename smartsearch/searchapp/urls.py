from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'searchapp'

urlpatterns = [
    path('', login_required(views.index.as_view()), name='home-page'),
    path('search/', views.SearchView.as_view(), name="google-search-view"),
    path('home/', views.home),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='searchapp/login.html'), name='login'),
    path('result/', views.result),
]
