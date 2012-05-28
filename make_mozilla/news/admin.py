from django.contrib.gis import admin

from make_mozilla.news import models


class ArticleAdmin(admin.ModelAdmin):
    model = models.Article
    list_display = ('title', 'autor',)

admin.site.register(models.Article, ArticleAdmin)
