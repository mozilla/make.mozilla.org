import jingo
from django.http import Http404
from django.shortcuts import get_object_or_404
from make_mozilla.pages import models


def serve(request, path):

    path_parts = path.split('/')
    path_length = len(path_parts)
    tmp_path = ""

    # this allows for nested paths - /foo/bar/ for exmample
    for p in path_parts:
        page = get_object_or_404(models.Page, path=p)

        if path_length != 1:
            tmp_path = tmp_path + "/%s" % page.path
            if path == tmp_path.lstrip('/'):
                # paths match but we've got a root page at the end - this is bogus
                if not page.has_parent:
                    raise Http404
                # /foo/foo/ requested - this is bogus, no duped content please
                if page.parent.path != path_parts[-2]:
                    raise Http404

        else:
            # /foo/ being requested but we're expecting /foo/bar/
            if page.has_parent:
                raise Http404

    return jingo.render(request, 'pages/page.html', {
        'page': page,
    })
