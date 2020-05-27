from django.shortcuts import render
from django.urls import reverse_lazy

from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin

from .models import Article

class ArticleListView(ListView):
    model = Article
    template_name = 'filtered_articles/article_list.html'
    context_object_name = 'article_list'
    paginate_by = 12
    queryset = Article.objects.filter(status=Article.STATUS.published).order_by('-created')

class ArticleDetailView(UserPassesTestMixin, DetailView):
    model = Article
    template_name = 'filtered_articles/article_detail.html'
    context_object_name = 'article'

    def test_func(self):
        if self.get_object().status == Article.STATUS.published:
            return True
        elif self.request.user.has_perm('filtered_articles.view_unpublished_article'):
            return True
        else:
            return False

class ArticleCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "filtered_articles.add_article"
    model = Article
    fields = ['title', 'body', 'markup', 'status',]

class ArticleUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "filtered_articles.change_article"
    model = Article
    fields = ['title', 'body', 'markup', 'status', 'slug']

class ArticleDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "filtered_articles.delete_article"
    model = Article
    success_url = reverse_lazy('article-list')