from django.core.exceptions import SuspiciousOperation
from django.core.files.base import ContentFile
from django.db import models
from django.db.models.fields import files
from PIL import Image
import cStringIO

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ['^make_mozilla\.core\.fields\.SizedImageField'])


class SizedImageFieldFile(files.ImageFieldFile):

    def __init__(self, *args, **kwargs):
        super(SizedImageFieldFile, self).__init__(*args, **kwargs)

        self.sizes = self.field.sizes

        if self.sizes:
            path, extension = self.url.rsplit('.', 1)

            for name, size in self.sizes.items():
                try:
                    width, height = self.get_width_height(size)

                    setattr(self, '%s_url' % name,
                        '%s.%s.%s' % (path, name, extension))
                    setattr(self, '%s_width' % name, width)
                    setattr(self, '%s_height' % name, height)
                except IOError:
                    pass
                except SuspiciousOperation:
                    pass

    def generate_thumb(self, img, width, height, format):
        img.seek(0)
        image = Image.open(img)
        image_width, image_height = image.size
        meta = image.info

        if height is None:
            height = width/float(image_width) * image_height

        maxfactor = max(width/float(image_width), height/float(image_height))
        w = round(image_width * maxfactor)
        h = round(image_height * maxfactor)

        print image_width, image_height, width, height, w, h

        image = image.resize((w, h), Image.ANTIALIAS)

        x = round((w-width)/2.0)
        y = round((h-height)/2.0)
        image = image.crop((x, y, w-x, h-y))
        image.load()

        image = image.resize((width, height), Image.ANTIALIAS)
        image.thumbnail((width, height), Image.ANTIALIAS)

        io = cStringIO.StringIO()
        format = 'jpeg' if format.lower() == 'jpg' else format.lower()
        image.save(io, format, **meta)

        return ContentFile(io.getvalue())

    def get_width_height(self, size):
        try:
            width = int(size)
            try:
                height = width / float(self.width) * self.height
            except IOError:
                height = None
        except TypeError:
            width = size[0]
            height = size[1]

        return (width, height)

    def save(self, name, content, save=True):
        super(SizedImageFieldFile, self).save(name, content, save)

        if self.sizes:
            path, extension = self.name.rsplit('.', 1)

            for name, size in self.sizes.items():
                width, height = self.get_width_height(size)
                target = '%s.%s.%s' % (path, name, extension)
                thumb = self.generate_thumb(content, width, height, extension)

                self.storage.save(target, thumb)

    def delete(self, save=True):
        super(SizedImageFieldFile, self).delete(save)

        if self.sizes:
            path, extension = self.name.rsplit('.', 1)
            for name in self.sizes:
                try:
                    self.storage.delete('%s.%s.%s' % (path, name, extension))
                except:
                    pass

class SizedImageField(models.ImageField):

    attr_class = SizedImageFieldFile

    def __init__(self, *args, **options):

        self.sizes = options.pop('sizes', None)

        super(SizedImageField, self).__init__(*args, **options)
