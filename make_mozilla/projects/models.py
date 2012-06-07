import hashlib
import urllib
from django.utils.safestring import mark_safe
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse
from django.db import models
from make_mozilla import tools
from make_mozilla import events
from make_mozilla.core import fields


class Project(models.Model):
    name = models.CharField(max_length=255)
    teaser = models.TextField()
    body = models.TextField(blank=True, null=True)
    url_hash = models.CharField(max_length=20, blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True)
    link = models.URLField(blank=True, null=True)
    featured = models.BooleanField(default=False)
    image = fields.SizedImageField(
        upload_to='projects',
        storage=FileSystemStorage(**settings.UPLOADED_IMAGES),
        sizes={
            'poster': 515,
            'flyer': (270, 165),
            'featured': (200, 130),
            'thumb': (126, 77),
        })

    contributor = models.ForeignKey('Contributor', blank=True, null=True)
    difficulties = models.ManyToManyField('Difficulty', blank=True, null=True)
    topics = models.ManyToManyField('Topic', blank=True, null=True)
    tools = models.ManyToManyField(tools.models.Tool, blank=True, null=True)
    skills = models.ManyToManyField('Skill', blank=True, null=True)

    class Meta:
        ordering = ['-added',]

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Project, self).save(*args, **kwargs)
        if not self.url_hash:
            # We have to do this after a save, because we need an ID from the DB
            self.url_hash = hashlib.sha224('%d' % self.id).hexdigest()[:9]
            self.save()

    @models.permalink
    def get_absolute_url(self):
        if self.hash == 'submit':
            return ('project.submit', (), {})
        return ('project', (), {'project_hash': self.hash})

    @property
    def content(self):
        if self.steps.count():
            content = '\n\n'.join(self.steps.values_list('content', flat=True))
        elif self.body:
            content = self.body
        else:
            content = self.teaser
        return mark_safe(content)

    @property
    def hash(self):
        if not self.url_hash:
            self.save()
        return self.url_hash

    @property
    def previous(self):
        try:
            return self.get_previous_by_added(difficulty=self.difficulty)
        except self.DoesNotExist:
            return None

    @property
    def next(self):
        try:
            return self.get_next_by_added(difficulty=self.difficulty)
        except self.DoesNotExist:
            return None


class ProjectStep(models.Model):
    project = models.ForeignKey('Project', related_name='steps')
    content = models.TextField()


class ProjectTag(models.Model):
    label = models.CharField(max_length=100)
    value = models.SlugField()
    index = models.IntegerField(max_length=2, default=1)

    class Meta:
        abstract = True
        ordering = ['index', 'id']

    def __unicode__(self):
        return self.label

    def get_absolute_url(self):
        url = reverse('projects')
        query = urllib.urlencode(dict([[self._meta.verbose_name, self.value]]))
        return '%s?%s' % (url, query)


class Difficulty(ProjectTag):
    class Meta:
        verbose_name_plural = 'difficulties'


class Topic(ProjectTag):
    pass


class Skill(ProjectTag):
    pass


class Contributor(models.Model):
    local_name = models.CharField(max_length=255, verbose_name='Name')
    partner = models.ForeignKey(events.models.Partner, blank=True, null=True)

    def __unicode__(self):
        return self.name

    @property
    def name(self):
        if self.partner:
            return self.partner.name
        return self.local_name

    @property
    def website(self):
        if self.partner:
            return self.partner.website
        return none

    @property
    def logo(self):
        if self.partner:
            return self.partner.logo
        return None