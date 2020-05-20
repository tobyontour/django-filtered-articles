from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('new', views.ArticleCreateView.as_view(), name='article-create'),
    path('<slug:slug>', views.ArticleDetailView.as_view(), name='article-detail'),
    path('<slug:slug>/edit', views.ArticleUpdateView.as_view(), name='article-update'),
    path('<slug:slug>/delete', views.ArticleDeleteView.as_view(), name='article-delete'),
    path('', views.ArticleListView.as_view(), name='article-list'),
]