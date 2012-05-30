from django.contrib.gis import admin
from make_mozilla.tools import models


class ToolAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',),}


admin.site.register(models.Tool, ToolAdmin)