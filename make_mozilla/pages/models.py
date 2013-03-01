from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from make_mozilla.core import fields


class Page(models.Model):
    title = models.CharField(max_length=255)
    path = models.SlugField()
    real_path = models.CharField(max_length=1024, unique=True, blank=True)
    parent = models.ForeignKey('self', blank=True, null=True,
        help_text='This will allow you to use URLs like /about/foo - parent.path + path',
        related_name='children')
    show_subnav = models.BooleanField(default=False,
        verbose_name='Show sub-navigation menu')
    subnav_title = models.CharField(max_length=100, blank=True, null=True,
        verbose_name='Menu title', help_text='This can be left blank if you do not need a title')
    additional_content = models.TextField(blank=True, null=True)

    def has_ancestor(self, page):
        if not self.parent:
            return False
        if self.parent.id == page.id:
            return True
        return self.parent.has_ancestor(page)

    def clean(self):
        from django.core.exceptions import ValidationError

        self.path = self.path.strip('/')

        if self.parent:
            if self.parent.has_ancestor(self):
                raise ValidationError('Cannot set page parent to one of its descendants')

            self.real_path = '%s/%s' % (self.parent.real_path, self.path)
        else:
            self.real_path = self.path

        try:
            if Page.objects.exclude(id__exact=self.id).get(real_path=self.real_path):
                raise ValidationError('This path/parent combination already exists.')
        except Page.DoesNotExist:
            # We can safely ignore this, as it means we're in the clear and our path is fine
            pass

    def save(self, *args, **kwargs):
        super(Page, self).save(*args, **kwargs)

        # Now we tell our children to update their real paths
        # This will happen recursively, so we don't need to worry about that logic here
        for child in self.children.all():
            child.real_path = '%s/%s' % (self.real_path, child.path)
            child.save()

    def __unicode__(self):
        return self.title

    @property
    def indented_title(self):
        indent = len(self.real_path.split('/')) - 1
        if not indent:
            return self.title
        return '%s %s' % ('-' * indent, self.title)


class PageSection(models.Model):
    title = models.CharField(max_length=255)
    subnav_title = models.CharField(max_length=255, blank=True, null=True,
        verbose_name='Sub-navigation title', help_text='Will use the section title if blank')
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
    def nav_title(self):
        if self.subnav_title:
            return mark_safe(self.subnav_title)
        return unicode(self)

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
