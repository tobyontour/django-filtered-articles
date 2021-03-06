from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from ..models import Article

User = get_user_model()

class ArticleTest(TestCase):

    def setUp(self):
        user = User.objects.create_user('testuser', email='testuser@example.com', password='testuser')
        user.first_name = 'John'
        user.last_name = 'Doe'
        permission = Permission.objects.get(codename='add_article')
        user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='change_article')
        user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='delete_article')
        user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='view_article')
        user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='view_unpublished_article')
        user.user_permissions.add(permission)
        user.save()

        user = User.objects.create_user('testuser2', email='testuser2@example.com', password='testuser2')
        user.first_name = 'Jane'
        user.last_name = 'Doe'
        permission = Permission.objects.get(codename='view_article')
        user.user_permissions.add(permission)
        user.save()
        article = Article.objects.create(
            title='First blog post',
            body="# First blog post\nFirst paragraph.",
            author=user
        )
        article.save()

    def test_anonymous_user_cant_create_article(self):
        response = self.client.get(reverse('article-create'))
        self.assertEqual(response.status_code, 302)

    def test_anonymous_user_cant_delete_article(self):
        response = self.client.get(reverse('article-delete', kwargs={'slug': 'first-blog-post'}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Article.objects.filter(slug='first-blog-post').exists())

    def test_anonymous_user_cant_update_article(self):
        response = self.client.get(reverse('article-update', kwargs={'slug': 'first-blog-post'}))
        self.assertEqual(response.status_code, 302)

    def test_normal_user_cant_create_article(self):
        self.client.login(username="testuser2", password="testuser2")
        response = self.client.get(reverse('article-create'))
        self.assertEqual(response.status_code, 403)

    def test_normal_user_cant_delete_article(self):
        self.client.login(username="testuser2", password="testuser2")
        response = self.client.get(reverse('article-delete', kwargs={'slug': 'first-blog-post'}))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Article.objects.filter(slug='first-blog-post').exists())

    def test_normal_user_cant_update_article(self):
        self.client.login(username="testuser2", password="testuser2")
        response = self.client.get(reverse('article-update', kwargs={'slug': 'first-blog-post'}))
        self.assertEqual(response.status_code, 403)

    def test_editor_user_can_access_create_article_form(self):
        self.client.login(username="testuser", password="testuser")
        response = self.client.get(reverse('article-create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'type="submit"')

    def test_editor_user_can_create_article(self):
        self.client.login(username="testuser", password="testuser")
        response = self.client.post(reverse('article-create'),
            {
               'title': 'New article',
               'body': '# New article body',
               'status': 'draft',
               'markup': 'txt',
               'slug': ''
            },
            follow=True)
        self.assertEqual(response.status_code, 200)

        article = Article.objects.filter(slug='new-article')[0]
        self.assertEqual(article.body, "# New article body")
        self.assertEqual("# New article body", article.get_filtered_body())
        self.assertEqual(article.slug, 'new-article')
        self.assertEqual(article.status, 'draft')
        self.assertEqual(article.markup, 'txt')

    def test_editor_user_can_update_article(self):
        self.client.login(username="testuser", password="testuser")
        response = self.client.post(reverse('article-update', kwargs={'slug': 'first-blog-post'}),
            {
               'title': 'New article',
               'body': '# New article body',
               'status': 'draft',
               'markup': 'txt',
               'slug': 'new-article'
            },
            follow=True)
        self.assertEqual(response.status_code, 200)

        article = Article.objects.filter(slug='new-article')[0]
        self.assertEqual(article.body, "# New article body")
        self.assertEqual("# New article body", article.get_filtered_body())
        self.assertEqual(article.slug, 'new-article')
        self.assertEqual(article.status, 'draft')
        self.assertEqual(article.markup, 'txt')

    def test_editor_user_can_delete_article(self):
        self.client.login(username="testuser", password="testuser")
        response = self.client.post(
            reverse('article-delete', kwargs={'slug': 'first-blog-post'}),
            follow=True)
        self.assertEqual(response.status_code, 200)

        self.assertFalse(Article.objects.filter(slug='first-blog-post').exists())

