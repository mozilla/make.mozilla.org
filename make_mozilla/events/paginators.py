from django.core.paginator import Paginator, Page, EmptyPage, PageNotAnInteger
from django.utils.safestring import mark_safe
from urllib import urlencode


class EventPaginator(Paginator):
    def __init__(self, object_list, per_page, orphans=0, allow_empty_first_page=True, adjacent_pagination_limit=3):
        super(EventPaginator, self).__init__(object_list, per_page, orphans, allow_empty_first_page)
        self.adjacent_pagination_limit = adjacent_pagination_limit

    def page(self, number):
        "Returns a Page object for the given 1-based page number."
        number = self.validate_number(number)
        bottom = (number - 1) * self.per_page
        top = bottom + self.per_page
        if top + self.orphans >= self.count:
            top = self.count
        return EventPage(self.object_list[bottom:top], number, self)


class EventPage(Page):
    def pagination_start(self):
        return max(1, self.number - self.paginator.adjacent_pagination_limit)

    def pagination_end(self):
        return min(self.paginator.num_pages, self.number + self.paginator.adjacent_pagination_limit)

    def pagination_item(self, base, number, sort, class_name='', content='', **query):
        href = base

        if number > 1:
            query['page'] = number
        if sort:
            query['sort'] = sort

        query_string = urlencode(query)

        if query_string:
            href += '?%s' % query_string

        if class_name:
            class_name = ' class="%s"' % class_name

        if not content:
            content = '<span>Page </span>%d' % number

        return '<li%s><a href="%s">%s</a></li>' % (
            class_name,
            href,
            content,
        )

    def pagination(self, base, sort='', query={}):
        start = self.pagination_start()
        end = self.pagination_end()
        items = []

        previous = '&nbsp; &laquo; &nbsp;'
        next = '&nbsp; &raquo; &nbsp;'

        # Previous arrow - check if we're at the first page
        if self.number == 1:
            items.append('<li class="previous">%s</li>' % previous);
        else:
            items.append(self.pagination_item(base, self.number - 1, sort, 'previous', previous, **query))

        # If the 'first' page isn't the first page, add an empty separator
        if start > 1:
            # Add the first page in if it's not already included
            if start > 2:
                items.append(self.pagination_item(base, 1, sort, **query))
            items.append('<li class="empty">...</li>')

        for number in range(start, end + 1):
            class_name = 'current' if number == self.number else ''
            items.append(self.pagination_item(base, number, sort, class_name, **query))

        # If the 'last' page isn't the last page, add an empty separator
        if (end < self.paginator.num_pages):
            items.append('<li class="empty">...</li>')
            # Add the last page in if it's not already included
            if end < self.paginator.num_pages - 1:
                items.append(self.pagination_item(base, self.paginator.num_pages, sort, **query))

        # Next link - check if we're at the last page
        if self.number == self.paginator.num_pages:
            items.append('<li class="next">%s</li>' % next);
        else:
            items.append(self.pagination_item(base, self.number + 1, sort, 'next', next, **query))

        return mark_safe(''.join(items))


def results_page(result_set, results_per_page, page = 1):
    paginator = EventPaginator(result_set, results_per_page)
    try:
        page = paginator.page(page)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page
