from django.shortcuts import get_object_or_404
import jingo
from make_mozilla import projects
from make_mozilla.tools import models


def index_static(request):
    thimble_projects = projects.models.Project.objects.filter(tool__slug='thimble').order_by('?')[:3]
    goggles_projects = projects.models.Project.objects.filter(tool__slug='x-ray-goggles').order_by('?')[:3]
    popcorn_projects = projects.models.Project.objects.filter(tool__slug='popcorn').order_by('?')[:3]

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