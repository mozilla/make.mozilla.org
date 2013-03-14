import jingo
from datetime import datetime

from django.conf import settings
from django.http import HttpResponse

from make_mozilla.news.models import Article
from make_mozilla.projects.models import Project
from make_mozilla.events.models import Event


def index(request):
    news = Article.objects.filter(featured=True).order_by('-updated')[0:3]
    projects = Project.objects.public_projects().filter(featured=True).order_by('?')[0:5]
    now = datetime.utcnow()
    events = Event.objects.filter(
            official=True
        ).filter(
            end__gte=now
        ).order_by(
            'start'
        )[0:3]
    return jingo.render(request, 'splash.html', {
        'news': news,
        'projects': projects,
        'events': events,
    })


def robots(request):
    hidden_projects = Project.objects.filter(public=False)
    context = {
        'DEBUG': settings.DEBUG,
        'hidden_projects': hidden_projects,
    }
    template = jingo.render(request, 'robots.txt', context)

    return HttpResponse(template, mimetype="text/plain")


def fail(request):
    return jingo.render(request, 'base/404.html', {}, status=404)


def app_fail(request):
    return jingo.render(request, 'base/500.html', {}, status=500)
