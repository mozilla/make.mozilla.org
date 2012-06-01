from django.contrib.gis import admin
from make_mozilla.projects import models


class ProjectStepInline(admin.TabularInline):
    model = models.ProjectStep


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'featured', )
    list_editable = ('featured', )
    list_filter = ('contributor', 'audience', 'tool', 'difficulty', 'skills', )
    exclude = ('url_hash',)
    # inlines = [ProjectStepInline,]


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'value':('label',),}


class AudienceAdmin(TagAdmin):
    pass


class DifficultyAdmin(TagAdmin):
    pass


class SkillAdmin(TagAdmin):
    pass


class ContributorAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.Audience, AudienceAdmin)
admin.site.register(models.Difficulty, DifficultyAdmin)
admin.site.register(models.Skill, SkillAdmin)
admin.site.register(models.Contributor, ContributorAdmin)
