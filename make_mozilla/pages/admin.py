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

        # Get all the pages, excluding ourself
        pages = models.Page.objects.exclude(id=self.instance.id).order_by('real_path')

        # Exclude all pages that are our descendants
        choices = [(page.id, page.indented_title) for page in pages
                        if not page.has_ancestor(self.instance)]

        # Put the null option back into the list
        choices.insert(0, ('', '---------'))

        # Set choices to correctly available pages
        self.fields['parent'].choices = choices


class PageAdmin(admin.ModelAdmin):
    def indented_title(page):
        return page.indented_title
    indented_title.short_description = 'Title'

    form = PageAdminForm
    ordering = ('real_path',)
    inlines = [PageSectionInline]
    prepopulated_fields = {'path': ('title',)}
    list_display = (indented_title, 'path', )
    fieldsets = (
        (None, {
            'fields': ('title', 'path', 'parent',),
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
