from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models import Article

User = get_user_model()

# Create your tests here.
class ArticleViewTest(TestCase):

    def setUp(self):
        user = User.objects.create_user('testuser', email='testuser@example.com', password='testuser')
        user.save()

        for i in range(0, 20):
            article = Article.objects.create(
                title=f'Blog post {i}',
                body="Generic paragraph.",
                author=user,
                status=Article.STATUS.published
            )
            if i == 0:
                article.status=Article.STATUS.draft
            article.save()

    def test_article_list_view(self):
        # Assumes paginate_by is 12
        response = self.client.get(reverse('article-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Blog post 19')
        self.assertContains(response, 'Blog post 18')
        self.assertContains(response, 'Blog post 8')
        self.assertNotContains(response, 'Blog post 7')
        self.assertContains(response, 'Page 1 of 2')

    def test_article_list_does_not_contain_unpublished(self):
        response = self.client.get(reverse('article-list') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Blog post 0')
        self.assertContains(response, 'Page 2 of 2')




