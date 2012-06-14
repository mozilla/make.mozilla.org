from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from make_mozilla.core import fields


class Page(models.Model):
    title = models.CharField(max_length=255)
    path = models.SlugField(unique=True)
    additional_content = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.title


class PageSection(models.Model):
    title = models.CharField(max_length=255)
    page = models.ForeignKey('Page', related_name='sections')
    poster = fields.SizedImageField(
        blank=True,
        null=True,
        upload_to='pages',
        storage=FileSystemStorage(**settings.UPLOADED_IMAGES),
        sizes={
            'standard': 900,
            'tablet': 700,
            'handheld': 500,
        })
    content = models.TextField()
    sidebar = models.TextField(blank=True, null=True)
    quotes = models.ManyToManyField('Quote', blank=True, null=True)

    class Meta:
        verbose_name = 'section'
        ordering = ['id']

    def __unicode__(self):
        return mark_safe(self.title)

    @property
    def has_sidebar(self):
        return self.sidebar or self.quotes.count()


class Quote(models.Model):
    quote = models.CharField(max_length=1000)
    source = models.ForeignKey('QuoteSource', blank=True, null=True)
    url = models.URLField(blank=True, null=True, verbose_name='URL')
    show_source_image = models.BooleanField(default=False, help_text='Show the source\'s image next to this quote, if available')

    @property
    def clean_quote(self):
        return strip_tags(self.quote)

    def __unicode__(self):
        quote = self.clean_quote
        if len(quote) > 25:
            quote = quote[:25] + '...'
        if not self.source:
            return quote
        return '%s (%s)' % (quote, self.source.name)


class QuoteSource(models.Model):
    name = models.CharField(max_length=255)
    strapline = models.CharField(max_length=255, blank=True, null=True, help_text='"Teacher", "CEO, MegaCorp", ...')
    url = models.URLField(blank=True, null=True, verbose_name='URL')
    avatar = fields.SizedImageField(
        blank=True,
        null=True,
        verbose_name='Image',
        upload_to='avatars',
        storage=FileSystemStorage(**settings.UPLOADED_IMAGES),
        sizes={
            'adjusted': (90,90),
        })

    class Meta:
        verbose_name = 'source'

    def __unicode__(self):
        if self.strapline:
            return '%s - %s' % (self.name, self.strapline)
        return self.name
