from django.shortcuts import render
from django.core.paginator import Paginator

from src.barrel_finder.models import Ad


def index_view(request):
    latest = Ad.objects.order_by('-date').all()[:10]
    return render(request, 'barrel_finder/index.html', {'latest': latest})


def list_view(request, page=1, category_slug = None):
    items = Ad.objects.order_by('-date').all()
    paginator = Paginator(items, 25)
    page_obj = paginator.get_page(page)
    page_obj.adjusted_elided_pages = paginator.get_elided_page_range(page)

    return render(request, 'barrel_finder/list.html', {
        'page_obj': page_obj,
        'category_slug': category_slug
    })
