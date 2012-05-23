from django.shortcuts import get_object_or_404
import jingo
from make_mozilla.projects import models


def index(request):
    projects = models.Project.objects.all()

    return jingo.render(request, 'projects/index.html', {
        'projects': projects
    })


def details(request, slug):
    project = get_object_or_404(models.Project, slug=slug)

    return jingo.render(request, 'projects/detail.html', {
        'project': project
    });
