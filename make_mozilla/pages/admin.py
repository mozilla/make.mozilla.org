from django import forms
from django.contrib import admin
from make_mozilla.pages import models, utils


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
        # Populate the parent values with pages that are not part of the
        # instance tree.
        descendants = utils.get_page_descendants(self.instance)
        ids = [d.id for d in descendants] + [self.instance.id]
        pages = (models.Page.objects.exclude(id__in=ids)
                 .order_by('real_path'))
        choices = [(page.id, page.indented_title) for page in pages]
        # Put the null option back into the list
        choices.insert(0, ('', '---------'))
        # Set choices to correctly available pages
        self.fields['parent'].choices = choices

    def clean_parent(self):
        """Validate that the ``parent`` is not:
        - Its own parent.
        - Part of the existing tree.
        """
        parent = self.cleaned_data.get('parent')
        if not parent:
            return
        if parent == self.instance:
            raise forms.ValidationError("Page can't be its own parent")
        # The parent can't be part of the same tree.
        # Retrieve all the descendants from the root of this instance.
        # If any of the ancestor of the parent are part of this tree
        # the parent will show up when walking the root of he instance tree.
        try:
            root = utils.get_page_root(self.instance)
        except ValueError, e:
            # An existing circular dependency detected in
            # the instance structure.
            raise forms.ValidationError(e)
        descendants = utils.get_page_descendants(root)
        if parent in descendants:
            raise forms.ValidationError("Pae is already page of "
                                        "this path structure.")
        # Because the children of the parent-to-be can have a single
        # parent they can't be part of the existing tree.
        return parent


def indented_title(page):
    return page.indented_title
indented_title.short_description = 'Title'


class PageAdmin(admin.ModelAdmin):

    form = PageAdminForm
    ordering = ('real_path',)
    inlines = [PageSectionInline]
    prepopulated_fields = {'path': ('title',)}
    list_display = (indented_title, 'real_path', )
    readonly_fields = ('real_path', )
    fieldsets = (
        (None, {
            'fields': ('title', 'path', 'parent', 'real_path', ),
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

    def save_model(self, request, obj, form, change):
        # Request for the children to be updated.
        obj.save(update_children=True)


class QuoteAdmin(admin.ModelAdmin):
    list_display = ('clean_quote', 'source',)
    list_filter = ('source',)


class QuoteSourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'strapline',)


admin.site.register(models.Page, PageAdmin)
admin.site.register(models.Quote, QuoteAdmin)
admin.site.register(models.QuoteSource, QuoteSourceAdmin)
