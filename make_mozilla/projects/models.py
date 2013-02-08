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
    slug = models.SlugField(unique=True, default='')
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

    def __init__(self, *args, **kwargs):
        super(Project, self).__init__(*args, **kwargs)
        if not self.slug and self.url_hash:
            self.slug = self.url_hash

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Project, self).save(*args, **kwargs)
        if not self.url_hash:
            # We have to do this after a save, because we need an ID from the DB
            self.url_hash = hashlib.sha224('%d' % self.id).hexdigest()[:9]
            if not self.slug:
                self.slug = self.url_hash
            self.save()

    def get_absolute_url(self):
        if self.hash == 'submit':
            return self.link
        return reverse('project', kwargs={'slug': self.slug})

    @property
    def groups(self):
        try:
            return self.group_set.all()
        # because we have the 'dummy project' that doesn't have a primary key
        except ValueError:
            return None

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
            return self.get_previous_by_added(difficulties__in=self.difficulties.all())
        except self.DoesNotExist:
            return None

    @property
    def next(self):
        try:
            return self.get_next_by_added(difficulties__in=self.difficulties.all())
        except self.DoesNotExist:
            return None


class Group(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, default='',
        help_text="Remember if you change this after a group has been saved it can cause broken links")
    members = models.ManyToManyField(Project, through='GroupMembership')
    body = models.TextField(null=True, blank=True,
        help_text='Please paste your HTML in here - please remember to include any images behind an HTTPS server')
    body_text_template = models.CharField(max_length=255, blank=True, null=True,
        help_text="If supplying an HTML template for the body include the filename here. We look for templates in 'make_mozilla/projects/templates/groups/'")
    take_body_from = models.CharField(max_length=4, choices=(
            ('body', 'body'),
            ('temp', 'body_text_template')
        ),
        default='body',
        help_text='Do you want the introduction text to be taken direct from the DB or from an HTML template file?')
    image = fields.SizedImageField(
        upload_to='projects',
        help_text='Unless custom CSS is written this will appear in the top right of the page, next to the title',
        storage=FileSystemStorage(**settings.UPLOADED_IMAGES),
        sizes={
            'poster': 515,
            'flyer': (270, 165),
            'featured': (200, 130),
            'thumb': (126, 77),
        })

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('group', kwargs={'slug': self.slug})

    @property
    def projects(self):
        return self.members.all().order_by('groupmembership__order')


class GroupMembership(models.Model):
    project = models.ForeignKey(Project)
    group = models.ForeignKey(Group)
    order = models.IntegerField(max_length=2, default=1,
        help_text="Order can also be set on the listing page once saved")


class ProjectStep(models.Model):
    project = models.ForeignKey('Project', related_name='steps')
    content = models.TextField()


class ProjectTag(models.Model):
    label = models.CharField(max_length=100)
    value = models.SlugField()
    index = models.IntegerField(max_length=2, default=1)

    class Meta:
        abstract = True
        ordering = ['index', 'label', 'id']

    def __unicode__(self):
        return self.label

    def get_absolute_url(self):
        url = reverse('projects')
        query = urllib.urlencode(dict([[self._meta.verbose_name, self.value]]))
        return '%s?%s' % (url, query)

    def get_project_filter_url(self):
        return self.get_absolute_url()


class Difficulty(ProjectTag):
    class Meta(ProjectTag.Meta):
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
        return None

    @property
    def logo(self):
        if self.partner:
            return self.partner.logo
        return None
