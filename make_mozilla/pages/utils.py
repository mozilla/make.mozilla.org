def update_children(page, prefix=None, walked_pages=None):
    """Update the ``real_path`` of the descendants of the given ``Page``."""
    walked_pages = walked_pages if walked_pages else []
    # Perfix used to determine the children path.
    page_segment = page.path
    if prefix:
        page_segment = prefix + '/' + page_segment
    page.real_path = page_segment
    page.save()
    for child in page.children.all():
        # Update the real path for this descendant.
        if child in walked_pages:
            # This page has been processed before, ignore.
            continue
        walked_pages.append(child)
        update_children(child, page_segment, walked_pages)
    return True


def get_page_root(page, walked_pages=None):
    """Dtermines the root of the given ``page`` if any."""
    walked_pages = walked_pages if walked_pages else []
    if not page.parent:
        # Item is the root because it has no parent.
        return page
    if page in walked_pages:
        # Page has been processed, this means a circular dependency.
        raise ValueError("Couldn't determine parent. Circular dependency "
                         "detected in %s" % page)
    walked_pages.append(page)
    return get_page_root(page.parent, walked_pages)


def get_page_descendants(page, children_pages=None):
    """Return a list of the children's page, walks the tree top-down."""
    children_pages = children_pages if children_pages else []
    for child in page.children.all():
        if child in children_pages:
            continue
        children_pages.append(child)
        get_page_descendants(child, children_pages)
    return children_pages
