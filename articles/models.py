import re, docutils.core
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from model_utils.models import TimeStampedModel
from model_utils.fields import StatusField
from model_utils import Choices
from markdown import markdown

User = get_user_model()

# Create your models here.
class Article(TimeStampedModel):
    PLAIN_TEXT = 'txt'
    MARKDOWN = 'mkd'
    RESTRUCTURED_TEXT = 'rst'

    MARKUP_CHOICES = [
        (PLAIN_TEXT, 'Plain text'),
        (MARKDOWN, 'Markdown'),
        (RESTRUCTURED_TEXT, 'reStructuredText')
    ]

    markup = models.CharField(
        max_length=3,
        choices=MARKUP_CHOICES,
        default=PLAIN_TEXT,
    )

    STATUS = Choices('draft', 'published')
    status = StatusField(default='draft')

    author = models.ForeignKey(User, editable=False, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100)
    body = models.TextField()
    slug = models.SlugField(max_length=50, blank=True, unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article-detail', args=[self.slug])

    def get_filtered_body(self):
        if self.markup == self.MARKDOWN:
            return mark_safe(markdown(self.body))
        elif self.markup == self.RESTRUCTURED_TEXT:
            return mark_safe(docutils.core.publish_parts(self.body, writer_name='html')['html_body'])
        else:
            return self.body

    def save(self, *args, **kwargs):
        self._make_unique_slug()
        super().save(*args, **kwargs)

    def _make_unique_slug(self):
        if self.slug == "":
            slug = slugify(self.title)
            if Article.objects.filter(slug=slug).exists():
                slugs = [a.slug for a in Article.objects.filter(slug__startswith=slug[:-4])]
                for i in range(1, 100):
                    slug = slug[:-4] + '-{:0>3d}'.format(i)
                    if slug not in slugs:
                        break

            self.slug = slug
