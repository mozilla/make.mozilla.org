from django.shortcuts import get_object_or_404
import jingo
from make_mozilla import projects
from make_mozilla.tools import models


def index_static(request):
    thimble_qs = models.Tool.objects.filter(slug='thimble')
    thimble_projects = projects.models.Project.objects.filter(tools__in=thimble_qs).order_by('?')[:3]

    goggles_qs = models.Tool.objects.filter(slug='x-ray-goggles')
    goggles_projects = projects.models.Project.objects.filter(tools__in=goggles_qs).order_by('?')[:3]

    popcorn_qs = models.Tool.objects.filter(slug='popcorn')
    popcorn_projects = projects.models.Project.objects.filter(tools__in=popcorn_qs).order_by('?')[:3]

    return jingo.render(request, 'tools/index_static.html', {
        'projects': {
            'thimble': thimble_projects,
            'goggles': goggles_projects,
            'popcorn': popcorn_projects,
        }
    })


def index(request):
    return index_static(request)

    featured_tools = models.Tool.objects.filter(featured=True)
    live_tools = models.Tool.live(include_featured=False)
    in_progress_tools = models.Tool.in_progress(include_featured=False)
    coming_soon_tools = models.Tool.coming_soon(include_featured=False)

    return jingo.render(request, 'tools/index.html', {
        'tools': {
            'featured': featured_tools,
            'live': live_tools,
            'in_progress': in_progress_tools,
            'coming_soon': coming_soon_tools,
        }
    })


def details(request, slug):
    tool = get_object_or_404(models.Tool, slug=slug)

    return jingo.render(request, 'tools/detail.html', {
        'tool': tool
    });


def details_goggles(request):
    return jingo.render(request, 'tools/detail_goggles.html')


def details_goggles_install(request):
    return jingo.render(request, 'tools/detail_goggles_install.html')
