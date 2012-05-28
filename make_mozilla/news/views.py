import jingo


def index(request):
    return jingo.render(request, 'news/splash.html', {})
