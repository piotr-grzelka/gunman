from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from src.barrel_finder.models import Ad, Category


def index_view(request):
    latest = Ad.objects.order_by('-date').all()[:10]
    return render(request, 'barrel_finder/index.html', {'latest': latest})


def list_all_view(request, page=1):
    items = Ad.objects.order_by('-date').all()
    paginator = Paginator(items, 25)
    page_obj = paginator.get_page(page)
    page_obj.adjusted_elided_pages = paginator.get_elided_page_range(page)

    return render(request, 'barrel_finder/list-all.html', {
        'page_obj': page_obj,
    })


def list_category_view(request, category_slug, page=1):
    items = Ad.objects.order_by('-date').all()
    paginator = Paginator(items, 25)
    page_obj = paginator.get_page(page)
    page_obj.adjusted_elided_pages = paginator.get_elided_page_range(page)

    category = get_object_or_404(Category, slug=category_slug)

    return render(request, 'barrel_finder/list-category.html', {
        'page_obj': page_obj,
        'category': category
    })


def ad_view(request, ad_slug):
    ad = get_object_or_404(Ad, slug=ad_slug)
    return render(request, 'barrel_finder/ad.html', {'ad': ad})