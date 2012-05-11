from functools import partial
from hashlib import md5

import bleach
from django.conf import settings
from django.core.cache import cache
from django.utils.safestring import mark_safe


LONG_CACHE = 60 * 60 * 24 * 7

def cached_render(render_function, source, cache_tag, cache_time=LONG_CACHE):
    """Render a string through a function, using the cache for the result.
    
    The render_function argument should be a single-argument function taking a
    byte or Unicode string and returning a byte or Unicode string.
    
    The cache_tag parameter should be a byte string specific to the rendering
    function, so the cached result can survive restarts but two separate
    functions won't tread on each other's toes.
    
    The result will be returned as a SafeString or SafeUnicode, and so can be
    rendered directly as HTML.
    
    """
    # Make sure the cache key is a byte string, not a Unicode string
    encoded = source.encode('utf8') if isinstance(source, unicode) else source
    cache_key = md5(encoded).hexdigest() + str(cache_tag)
    
    cached = cache.get(cache_key)
    if cached:
        return mark_safe(cached)
    
    rendered = render_function(source)
    cache.set(cache_key, rendered, cache_time)
    return mark_safe(rendered)


# Generate a bleach cache tag that will be sensitive to changes in settings
_bleach_settings_string = str(settings.BLEACH.allowed_tags) + str(settings.BLEACH.allowed_attrs)
BLEACH_CACHE_TAG = md5(_bleach_settings_string).hexdigest()


def bleached(source):
    """Render a string through the bleach library, caching the result."""
    render_function = partial(bleach.clean,
                              tags=settings.BLEACH.allowed_tags,
                              attributes=settings.BLEACH.allowed_attrs)
    return cached_render(render_function, source, cache_tag=BLEACH_CACHE_TAG)
