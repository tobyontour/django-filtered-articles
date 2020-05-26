from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models import Article

User = get_user_model()

# Create your tests here.
class ArticleTest(TestCase):

    def setUp(self):
        user = User.objects.create_user('testuser', email='testuser@example.com', password='testuser')
        user.first_name = 'John'
        user.last_name = 'Doe'
        user.save()
        self.article = Article.objects.create(
            title='First blog post',
            body="# First blog post\nFirst paragraph.",
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


    def test_article(self):
        self.assertEqual(f'{self.article.title}', 'First blog post')
        self.assertEqual(f'{self.article.author.first_name}', 'John')
        self.assertEqual(f'{self.article.author.last_name}', 'Doe')
        self.assertEqual(f'{self.article.slug}', 'first-blog-post')
        self.assertEqual(f'{self.article.status}', Article.STATUS.draft)

    def test_article_body(self):
        article = Article.objects.filter(title='First blog post')[0]
        self.assertEqual(article.body, "# First blog post\nFirst paragraph.")
        self.assertEqual(article.get_filtered_body(), "# First blog post\nFirst paragraph.")


    def test_article_markdown_body(self):
        article = Article.objects.filter(title='Second blog post')[0]
        self.assertEqual(article.body, "# Second blog post\nFirst paragraph.")
        self.assertIn('<h1>Second blog post</h1>', article.get_filtered_body())
        self.assertIn('<p>First paragraph.</p>', article.get_filtered_body())
        self.assertEqual(article.slug, 'second-blog-post')

    def test_article_restructuredtext_body(self):
        article = Article.objects.filter(title='Third blog post')[0]
        self.assertEqual(article.body, "Third blog post\n===============\nFirst paragraph.")
        self.assertIn('<h1 class="title">Third blog post</h1>', article.get_filtered_body())
        self.assertIn('<p>First paragraph.</p>', article.get_filtered_body())
        self.assertEqual(article.slug, 'third-blog-post')

