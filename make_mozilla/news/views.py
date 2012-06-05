import jingo
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from make_mozilla.news.models import Article


def index(request):

    articles = Article.objects.all().order_by('-updated')
    paginator = Paginator(articles, 10)

    try:
        page = int(request.GET.get('page', '1'))
    except (ValueError, TypeError):
        page = 1

    try:
        paged_articles = paginator.page(page)
    except (EmptyPage, InvalidPage):
        paged_articles = paginator.page(paginator.num_pages)

    if paged_articles.number == 1:
        start_index = 1
    else:
        start_index = paged_articles.number * 10 - 9

    return jingo.render(request, 'news/splash.html', {
        'articles': paged_articles,
        'start_index': start_index
    })
