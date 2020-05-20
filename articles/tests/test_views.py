from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models import Article

User = get_user_model()

# Create your tests here.
class ArticleViewTest(TestCase):

    def setUp(self):
        user = User.objects.create_user('testuser', email='testuser@example.com', password='testuser')
        user.first_name = 'John'
        user.last_name = 'Doe'
        user.save()
        self.article = Article.objects.create(
            title='First blog post',
            body="First blog post\nFirst paragraph.",
            author=user
        )
        self.article.save()
        article = Article.objects.create(
            title='Second blog post',
            body="# Second blog post\nFirst paragraph.",
            author=user,
            markup=Article.MARKDOWN,
        )
        article.save()
        article = Article.objects.create(
            title='Third blog post',
            body="Third blog post\n===============\nFirst paragraph.",
            author=user,
            markup=Article.RESTRUCTURED_TEXT,
        )
        article.save()

    def test_article_list_view(self):
        response = self.client.get(reverse('article-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'First blog post')
        self.assertContains(response, 'Second blog post')
        self.assertContains(response, 'Third blog post')

    def test_article_detail_view_plain_text(self):
        response = self.client.get(reverse('article-detail', kwargs={'slug': 'first-blog-post'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<h2>First blog post</h2>')
        self.assertNotContains(response, 'Second blog post')
        self.assertContains(response, '<div class="article-body">First blog post\nFirst paragraph.</div>')

    def test_article_detail_view_markdown(self):
        response = self.client.get(reverse('article-detail', kwargs={'slug': 'second-blog-post'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<h2>Second blog post</h2>')
        self.assertNotContains(response, 'First blog post')
        self.assertContains(response, '<h1>Second blog post</h1>\n<p>First paragraph.</p>')

    def test_article_detail_view_restructuredtext(self):
        response = self.client.get(reverse('article-detail', kwargs={'slug': 'third-blog-post'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<h2>Third blog post</h2>')
        self.assertNotContains(response, 'First blog post')
        self.assertContains(response, '<h1 class="title">Third blog post</h1>\n<p>First paragraph.</p>')
