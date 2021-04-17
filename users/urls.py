from django.urls import path, re_path
from . import views
from .models import Profile
from django.contrib.auth import views as auth_views
#from .views import UserProfileView
app_name= 'users'

urlpatterns = [
    path('register', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='../templates/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='../templates/logout.html'), name='logout'),
    path('profile/',views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit-profile'),
    path('score-explained/', views.score_explained, name='score-explained'),

    #re_path('profile/id/(?P<slug>[\w.@+-]+)/$', UserProfileView.as_view(), name='profile'),
]



#url
#'profile/(?P<username>[a-zA-Z0-9]+)'
