from django.urls import path
from . import views
from django.shortcuts import redirect



app_name = 'pages'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('p/<slug:topic>/', views.ForumView.as_view(), name='forum'),  #name can be referenced in html templates and redirects
    #path('estimate/', views.EstimateListView.as_view(), name='estimate-list'),
    path('estimate/<int:pk>/', views.EstimateDetailView.as_view(), name='estimate-detail'),
    path('estimate/new/', views.EstimateCreateView.as_view(), name='estimate-create'),
    path('estimate/<int:pk>/update/', views.EstimateUpdateView.as_view(), name='estimate-update'),
    path('estimate/<int:pk>/delete/', views.EstimateDeleteView.as_view(), name='estimate-delete'),
    path('question/<int:pk>/<slug:slug>/update/', views.QuestionUpdateView.as_view(), name='question-update'),
    #path('question/', views.QuestionListView.as_view(), name='question-list'),
    #path('question/<int:pk>/', views.QuestionDetailView.as_view(), name='question-detail'),
    path('search/', views.searchbar, name='searchbar'),
    path('piechart/', views.piechart, name='piechart'),

    path('p/<slug:topic>/<int:pk>/<slug:slug>/', views.QuestionDetailView.as_view(), name='question-detail'),
    path('question/new/', views.QuestionCreateView.as_view(), name='question-create'),
    path('p/<slug:topic>/question/new/', views.QuestionCreateView.as_view(), name='question-create-forum'),

    path('question/<int:pk>/update/', views.QuestionUpdateView.as_view(), name='question-update'),
    path('question/<int:pk>/delete/', views.QuestionDeleteView.as_view(), name='question-delete'),
    path('tracked/',  views.TrackedQuestionsView.as_view(), name='estimate-list'),
    path('popular/',  views.PopularQuestionsView.as_view(), name='popular-list'),


    path('create/', views.CreateForumView.as_view(), name='create-subforum'),
    #path('<slug:slug>/', views.ForumDetailView.as_view() , name='forum_detail'),
    path('create/<slug:slug>/', views.ForumDetailView.as_view() , name='forum_create_success'),
    path('update/<slug:slug>/', views.ForumUpdateView.as_view() , name='forum_update'),  # pass attrs to method to changes

]
