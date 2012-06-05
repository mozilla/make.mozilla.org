import jingo

from make_mozilla.news.models import Article


def index(request):
    news = Article.objects.filter(featured=True).order_by('-updated')[0:3]
    return jingo.render(request, 'splash.html', {
        'news': news,
    })


def fail(request):
    return jingo.render(request, 'base/404.html', {}, status=404)


def app_fail(request):
    return jingo.render(request, 'base/500.html', {}, status=500)
