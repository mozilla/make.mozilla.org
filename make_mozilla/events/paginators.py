from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def results_page(result_set, results_per_page, page = 1):
    paginator = Paginator(result_set, results_per_page)
    try:
        page = paginator.page(page)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page
