from django.contrib.gis import admin

from make_mozilla.news import models


def make_featured(ModelAdmin, request, queryset):
    queryset.update(featured=True)
make_featured.short_description = "Mark selected stories as featured"


class ArticleAdmin(admin.ModelAdmin):
    model = models.Article
    list_display = ('title', 'autor', 'updated', 'featured',)
    list_filter = ('featured',)
    ordering = ['-updated']
    actions = [make_featured]

admin.site.register(models.Article, ArticleAdmin)
