from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from ..models import Article

User = get_user_model()

# Create your tests here.
class ArticleViewTest(TestCase):

    def setUp(self):
        user = User.objects.create_user('testuser', email='testuser@example.com', password='testuser')
        user.first_name = 'John'
        user.last_name = 'Doe'
        user.save()
        user2 = User.objects.create_user('testuser2', email='testuser2@example.com', password='testuser2')
        user2.first_name = 'Jane'
        user2.last_name = 'Doe'
        permission = Permission.objects.get(codename='view_unpublished_article')
        user2.user_permissions.add(permission)
        user2.save()
        self.article = Article.objects.create(
            title='First blog post',
            body="First blog post\nFirst paragraph.",
            author=user,
            status=Article.STATUS.published,
        )
        self.article.save()
        article = Article.objects.create(
            title='Second blog post',
            body="# Second blog post\nFirst paragraph.",
            author=user,
            markup=Article.MARKDOWN,
            status=Article.STATUS.published,
        )
        article.save()
        article = Article.objects.create(
            title='Third blog post',
            body="Third blog post\n===============\nFirst paragraph.",
            author=user,
            markup=Article.RESTRUCTURED_TEXT,
            status=Article.STATUS.published,
        )
        article.save()
        article = Article.objects.create(
            title='Unpublished blog post',
            body="Unpublished blog post",
            author=user,
            markup=Article.RESTRUCTURED_TEXT,
            status=Article.STATUS.draft,
        )
        article.save()

    def test_article_detail_view_plain_text(self):
        response = self.client.get(reverse('article-detail', kwargs={'slug': 'first-blog-post'}))
        self.assertEqual(200, response.status_code)
        self.assertContains(response, '<h2>First blog post</h2>')
        self.assertNotContains(response, 'Second blog post')
        self.assertContains(response, '<div class="article-body">First blog post\nFirst paragraph.</div>')

    def test_article_detail_view_markdown(self):
        response = self.client.get(reverse('article-detail', kwargs={'slug': 'second-blog-post'}))
        self.assertEqual(200, response.status_code)
        self.assertContains(response, '<h2>Second blog post</h2>')
        self.assertNotContains(response, 'First blog post')
        self.assertContains(response, '<h1>Second blog post</h1>\n<p>First paragraph.</p>')

    def test_article_detail_view_restructuredtext(self):
        response = self.client.get(reverse('article-detail', kwargs={'slug': 'third-blog-post'}))
        self.assertEqual(200, response.status_code)
        self.assertContains(response, '<h2>Third blog post</h2>')
        self.assertNotContains(response, 'First blog post')
        self.assertContains(response, '<h1 class="title">Third blog post</h1>\n<p>First paragraph.</p>')

    def test_anonymous_user_cant_access_unpublished_article(self):
        a = Article.objects.filter(slug='unpublished-blog-post').first()
        response = self.client.get(reverse('article-detail', kwargs={'slug': 'unpublished-blog-post'}))
        self.assertEqual(302, response.status_code)

    def test_normal_user_cant_access_unpublished_article(self):
        self.client.login(username="testuser", password="testuser")
        response = self.client.get(reverse('article-detail', kwargs={'slug': 'unpublished-blog-post'}))
        self.assertEqual(403, response.status_code)

    def test_editor_user_can_access_unpublished_article(self):
        self.client.login(username="testuser2", password="testuser2")
        response = self.client.get(reverse('article-detail', kwargs={'slug': 'unpublished-blog-post'}))
        self.assertEqual(200, response.status_code)
        self.assertContains(response, 'Unpublished blog post')
