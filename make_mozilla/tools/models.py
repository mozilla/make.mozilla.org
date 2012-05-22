from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models


TOOL_STATUS_CHOICES = (
    ('2', 'Live'),
    ('1', 'In Progress'),
    ('0', 'Coming Soon'),
)


class Tool(models.Model):
    name = models.CharField(max_length = 255)
    strapline = models.CharField(max_length = 100)
    url = models.URLField(blank = True)
    slug = models.SlugField()
    description = models.TextField(blank = True)
    featured = models.BooleanField(default = False)
    new = models.BooleanField(default = True)
    status = models.CharField(max_length = 1, choices = TOOL_STATUS_CHOICES)
    logo = models.ImageField(upload_to = 'tools', storage = FileSystemStorage(**settings.UPLOADED_IMAGES))

    @models.permalink
    def get_absolute_url(self):
        return ('tool', (), {'slug': self.slug})

    @classmethod
    def live(self, include_featured=True):
        tools = self.objects.filter(status='2')

        if not include_featured:
            tools = tools.filter(featured=False)

        return tools

    @classmethod
    def in_progress(self, include_featured=True):
        tools = self.objects.filter(status='1')

        if not include_featured:
            tools = tools.filter(featured=False)

        return tools

    @classmethod
    def coming_soon(self, include_featured=True):
        tools = self.objects.filter(status='0')

        if not include_featured:
            tools = tools.filter(featured=False)

        return tools

    def __unicode__(self):
        return self.name