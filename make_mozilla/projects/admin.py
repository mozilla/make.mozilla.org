from django.contrib.gis import admin
from make_mozilla.projects import models


class ProjectStepInline(admin.TabularInline):
    model = models.ProjectStep


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'featured', 'contributor', )
    list_editable = ('featured', )
    list_filter = ('contributor', 'difficulties', 'topics', 'tools', 'skills', )
    exclude = ('url_hash',)
    prepopulated_fields = {'slug': ('name',),}
    # inlines = [ProjectStepInline,]


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'value':('label',),}
    fieldsets = (
        (None, {
            'fields': ('label', 'value', ),
        }),
        ('Advanced', {
            'classes': ('collapse', ),
            'fields': ('index', ),
        })
    )


class GroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', ), }


class GroupMembershipAdmin(admin.ModelAdmin):
    list_display = ('project', 'group', 'order', )
    list_editable = ('order', )
    list_filter = ('group', )


class TopicAdmin(TagAdmin):
    pass


class DifficultyAdmin(TagAdmin):
    pass


class SkillAdmin(TagAdmin):
    pass


class ContributorAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.Group, GroupAdmin)
admin.site.register(models.GroupMembership, GroupMembershipAdmin)
admin.site.register(models.Topic, TopicAdmin)
admin.site.register(models.Difficulty, DifficultyAdmin)
admin.site.register(models.Skill, SkillAdmin)
admin.site.register(models.Contributor, ContributorAdmin)
