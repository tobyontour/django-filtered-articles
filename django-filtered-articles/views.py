from django.shortcuts import render
from django.urls import reverse_lazy

from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

from .models import Article

class ArticleListView(ListView):
    model = Article
    template_name = 'django-filtered-articles/article_list.html'
    context_object_name = 'article_list'
    paginate_by = 12

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'django-filtered-articles/article_detail.html'
    context_object_name = 'article'

class ArticleCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "django-filtered-articles.add_article"
    model = Article
    fields = ['title', 'body', 'markup', 'status',]

class ArticleUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "django-filtered-articles.change_article"
    model = Article
    fields = ['title', 'body', 'markup', 'status', 'slug']

class ArticleDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "django-filtered-articles.delete_article"
    model = Article
    success_url = reverse_lazy('article-list')