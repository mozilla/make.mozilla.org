from django.contrib.gis import admin
from make_mozilla.projects import models


admin.site.register(models.Project)