from django.urls import path
from .import views
from django.conf import settings

urlpatterns=[
    path('', views.welcome, name='welcome'),
    path('profile/', views.profile, name='profile'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('accounts/login', views.signin, name='login'),
    path('profile/<username>', views.profile, name='profile'),
    path('profile/<username>/edit', views.profile_edit, name='editProfile'),
]