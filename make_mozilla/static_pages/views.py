import jingo


def itu_index(request):
    return jingo.render(request, 'static_pages/itu_index.html', {})


def itu_kit(request):
    return jingo.render(request, 'static_pages/itu_kit.html', {})


def itu_advocates(request):
    return jingo.render(request, 'static_pages/itu_advocates.html', {})


def itu_videos(request):
    return jingo.render(request, 'static_pages/itu_videos.html', {})
