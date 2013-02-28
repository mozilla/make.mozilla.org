from django import forms
from django.contrib import admin
from make_mozilla.pages import models


class PageSectionInline(admin.StackedInline):
    model = models.PageSection
    extra = 1
    fieldsets = (
        (None, {
            'fields': ('title', 'subnav_title', 'poster', 'content',),
        }),
        ('Sidebar', {
            'classes': ('collapse',),
            'fields': ('quotes', 'sidebar',),
        }),
    )
    prepopulated_fields = {"subnav_title": ("title",)}
    filter_horizontal = ('quotes',)


class PageAdminForm(forms.ModelForm):
    class Meta:
        model = models.Page

    def __init__(self, *args, **kwargs):
        super(PageAdminForm, self).__init__(*args, **kwargs)
        # In theory this could be extended to preclude parent/child loops,
        # but that's an exercise left to the reader for now!
        self.fields['parent'].queryset = models.Page.objects.exclude(id__exact=self.instance.id)


class PageAdmin(admin.ModelAdmin):
    inlines = [PageSectionInline]
    prepopulated_fields = {'path': ('title',)}
    list_display = ('title', 'path',)
    fieldsets = (
        (None, {
            'fields': ('title', 'path',),
        }),
        ('Sub-navigation', {
            'classes': ('collapse',),
            'fields': ('show_subnav', 'subnav_title',),
        }),
        ('Advanced', {
            'classes': ('collapse',),
            'fields': ('additional_content',),
        }),
    )


class QuoteAdmin(admin.ModelAdmin):
    list_display = ('clean_quote', 'source',)
    list_filter = ('source',)


class QuoteSourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'strapline',)


admin.site.register(models.Page, PageAdmin)
admin.site.register(models.Quote, QuoteAdmin)
admin.site.register(models.QuoteSource, QuoteSourceAdmin)
