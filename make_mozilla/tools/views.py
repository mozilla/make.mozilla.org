from django.shortcuts import get_object_or_404
import jingo
from make_mozilla.tools import models


def index(request):
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