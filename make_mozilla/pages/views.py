import jingo
from django.shortcuts import get_object_or_404
from make_mozilla.pages import models


def serve(request, path):
    page = get_object_or_404(models.Page, real_path=path.strip('/'))

    return jingo.render(request, 'pages/page.html', {
        'page': page,
    })
